from __future__ import division, unicode_literals
import codecs
from bs4 import BeautifulSoup
import re
from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
import math
from helpers import lines, sentences, substrings
import random
import operator
import ast
from itertools import chain
import sys
import time
import binascii


def splitfile(file):
    n = 100
    chunks = [file[i:i+n] for i in range(0, len(file), n)]
    return chunks

def randomslicematch(inputlist, databasebinary, databaseverse, outputlist, recursiondepth):
    for y in range(0, len(inputlist)):
        rand = 0
        if len(inputlist) == 0:
            return outputlist
        if len(inputlist) > 3:
            rand = random.randrange(1, 4)
        elif len(inputlist) <= 4:
          rand = random.randrange(1, (len(inputlist) + 1))
        timeout = time.time() + .0001
        randomdatabaseindex = random.randrange(0, len(databasebinary))
        randomindexinindex = random.randrange(0, len(databasebinary[randomdatabaseindex]))
        if len(inputlist) == 1:
            slicetobefound = inputlist[0]
            while slicetobefound != databasebinary[randomdatabaseindex][randomindexinindex]:
                randomdatabaseindex = random.randrange(0, len(databasebinary))
                randomindexinindex = random.randrange(0, len(databasebinary[randomdatabaseindex]))
                if time.time() > timeout:
                    abort(400, f"no word found for ascii-as-binary slice: {slicetobefound}")
            slicetobefoundasverseword = databaseverse[randomdatabaseindex][randomindexinindex]
            outputlist.append(slicetobefoundasverseword)
            return outputlist
        slicetobefound = inputlist[0:rand]
        if len(slicetobefound) == 1:
            slicetobefound = slicetobefound[0]
        while slicetobefound != databasebinary[randomdatabaseindex][randomindexinindex]:
            randomdatabaseindex = random.randrange(0, len(databasebinary))
            randomindexinindex = random.randrange(0, len(databasebinary[randomdatabaseindex]))
            if time.time() > timeout:
                return randomslicematch(inputlist, databasebinary, databaseverse, outputlist, (recursiondepth + 1))
                #abort(400, f"no word found for ascii-as-binary slice2: {slicetobefound}")
        slicetobefoundasverseword = databaseverse[randomdatabaseindex][randomindexinindex]
        outputlist.append(slicetobefoundasverseword)
        inputlist = inputlist[rand:len(inputlist)]

# Two functions, both added 10/4/20, from mhawke's answer and comment here:
# https://stackoverflow.com/questions/40557335/binary-to-string-text-in-python
def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
def encode_string_binary(s):
    return ''.join([bin(ord(c))[2:].rjust(8,'0') for c in s])

# Function that lists duplicate items in a list, courtesy of PaulMcG's answer here:
# https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
def list_duplicates_of(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

# Flattens uneven, nested lists of three levels or fewer (e.g. [[0, 1, [0, 1], 0], [1, [0, 1]], ['cats']] becomes [0, 1, 0, 1, 0, 1, 0, 1, 'cats']
# (A surprisingly thorny problem, this.)
def flatten(l):
    flatl = l
    wordadditionscounter = 1
    for chunkline in l:
        sylladditionscounter = 0
        chunklineindex = l.index(chunkline)
        if type(chunkline) is list:
            for lineword in chunkline:
                linewordindex = chunkline.index(lineword)
                if type(lineword) is list:
                    for keywordsyllable in lineword:
                        keywordsyllableindex = lineword.index(keywordsyllable)
                        flatl[chunklineindex].insert(linewordindex + sylladditionscounter + 1, keywordsyllable)
                        sylladditionscounter += 1
                    del flatl[chunklineindex][linewordindex]
    for chunkline in l:
        wordadditionscounter -= 1
        chunklineindex = l.index(chunkline)
        if type(chunkline) is list:
            for lineword in chunkline:
                flatl.insert(chunklineindex + wordadditionscounter + 1, lineword)
                wordadditionscounter += 1
            del flatl[chunklineindex]
    return(flatl)

# Web app
app = Flask(__name__)


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Handle requests for / via GET (and POST)"""
    return render_template("index.html")


@app.route("/emphasize", methods=["POST"])
def emphasize():
    """Handle requests for /emphasize via POST"""

    # Read files
    if not request.files["file1"] or not request.files["file2"]:
        abort(400, "missing file")
    try:
        file1 = request.files["file1"].read().decode("utf-8")
        file2 = request.files["file2"].read().decode("utf-8")
    except Exception:
        abort(400, "invalid file")


    asciifileasbinary_master = encode_string_binary(file1)

    asciifileasbinary = splitfile(asciifileasbinary_master)

    # New list for scanned input. List structured first by the html "</p>" tag, because this seems to be how line breaks are tagged in html...
    # I should say: the way I am testing this is with two .rtf (textEdit) files: file1 is the python test code, file2 is the html rendition of a
    # .docx file containing the verse text original (in which "bolded" words or syllables represent STRESSED words or syllables).
    # To get this html version, I simply copy-and-pasted the .docx text into an online word-to-html converter. I then pasted the output
    # from this converter into that .rtf file which I uploaded as file2.
    # I will at some point need to come up with a method of automating this conversion from word-doc (or pdf) originals to html.
    # (Taking a step back, I want it in html, because with an html string I can work with both tags and whitespace, whereas with .docx
    # text I can only work with runs (see https://msdn.microsoft.com/en-us/library/office/gg278312.aspx). Moreover, conversion to html seems
    # to maintain, with zero or negligible error, bolded text from the .docx files and label it with the <b></b> tag.)
    # The split-around value I will use for this "file2.split(______)" will depend on how I automate the conversion of .docx (or .pdf or .rtf)
    # text to .html text, as it seems that different converters convert newlines differently. (I was, e.g., using "</div>" instead of "</p>"
    # in a test program.)
    scannedinputbylinesbywords = [x.split() for x in file2.split("</p>")]

    # Cleans up some stuff:
    scannedinputbylinesbywords = [[x for x in y if "\\" not in x] for y in scannedinputbylinesbywords]
    scannedinputbylinesbywords = [[x for x in y if "}" not in x] for y in scannedinputbylinesbywords]
    # Lot o' garbage!
    scannedinputbylinesbywords = [x for x in scannedinputbylinesbywords if x != []]

    ###### USE THIS PRINT: print(scannedinputbylinesbywords) ###### the 'if "\\" not in x' clause should perhaps be replaced by a more advanced
    ###### strip method that saves elements like, "<b>to\\'92t</b>," that contain both viable words and '\\.'
    # ^ What that comment to myself means is that apostrophed words like "to't" and "I'll" are missing in this version,
    # but not lost from our ambition, and never forgotten from our minds.
    # We will find them.
    # And we will render them in binary.

    # Reformats floating "</b>" tags (as in: ['this', '<b>is', '</b>', 'a']) (due to whitespace split).
    # And did same for "<b>" tags (even though bolded whitespace seems only to occur in the whitespace between the text and the TRAILING </b> tag).
    # ((Should fix this index-method also, as I did the pythoninputbychunksbylinesbykeywords for-loop above; mistakes in cases of duplicate words
    # per line —— granted, this is much rarer in English (esp. Shakespeare) than in python.))
    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line)
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word)
            if word == "</b>":
                # Literally pastes the </b> end-tag onto the end of the preceding word, and deletes the list-element that was previously occupied
                # by the </b> end-tag.
                q = scannedinputbylinesbywords[lineindex][wordindex - 1]
                scannedinputbylinesbywords[lineindex][wordindex - 1] = q + " </b>"
                scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])
            elif word == "<b>":
                q = scannedinputbylinesbywords[lineindex][wordindex + 1]
                scannedinputbylinesbywords[lineindex][wordindex + 1] = "<b>" + q
                scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])

    # Looks for words like '</b> the' and pushes the </b> tag back to the previous word, so that we have something like ['<b>What</b>', ' the']
    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line)
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word)
            wordaslist = list(word)
            if wordaslist[:4] == ['<', '/', 'b', '>']:
                prevwordaslist = list(scannedinputbylinesbywords[lineindex][wordindex-1])
                del wordaslist[:3]
                wordaslist[0] = ' '
                prevwordaslist.append("</b>")
                wordlistasstring = ''.join(wordaslist)
                prevwordlistasstring = ''.join(prevwordaslist)
                scannedinputbylinesbywords[lineindex][wordindex] = wordlistasstring
                scannedinputbylinesbywords[lineindex][wordindex-1] = prevwordlistasstring

    # gets rid of "<p>" tags ("</p>"s are gone from the split)
    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line)
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word)
            wordaslist = list(word)
            if wordaslist[:3] == ['<', 'p', '>']:
                del wordaslist[:2]
                wordaslist[0] = ' '
                wordlistasstring = ''.join(wordaslist)
                scannedinputbylinesbywords[lineindex][wordindex] = wordlistasstring

    # Creates binary list that is, so to speak, isomorphic to the list of the words of the original (following the floating-tag-reformatting above)
    # (Same thing as was done for the pythonbinary___ list-creation from the pythoninput___ original, above.)
    scannedbinarybylinesbywords = [[0 for x in y] for y in scannedinputbylinesbywords]
    # print(f"scannedbinarybylinesbywords before loop: {scannedbinarybylinesbywords}")

    # For-loop uses BeautifulSoup html scraper to identify occurences of the bold <b></b> tag and replace these occurences with 1's,
    # while still maintaining a list structure in which each line of verse is a list of words, and where multisyllabic words are sublists.
    # E.g.:
    # [['<b>This</b>', 'is', 'a', '<b>', 'bold</b>ed', '<b>text.</b>'], ['And', '<b>this', '</b>', 'is', '<b>too.</b></div>']]
    # became (from prev for-loop):
    # [['<b>This</b>', 'is', 'a', '<b>bold</b>ed', '<b>text.</b>'], ['And', '<b>this</b>', 'is', '<b>too.</b></div>']]
    # which, in the below for-loop, becomes:
    # [['<b>This</b>', 'is', 'a', [<b>bold</b>, 'ed'], '<b>text.</b>'], ['And', '<b>this</b>', 'is', '<b>too.</b></div>']]
    # Meanwhile,
    #          [[0, 0, 0, 0, 0], [0, 0, 0, 0]]
    # becomes: [[1, 0, 0, [1, 0], 1], [0, 1, 0, 1]]
    # Some fiddling with punctuation is necessary.
    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line)
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word)
            soup = BeautifulSoup(''.join(word), features="html5lib")
            # This "try-except" method came about because I want to strip the word down until it is of the form '<b>This</b>' or 'is,'
            # but the only way I know I have stripped it down (which I do with BeautifulSoup's "unwrap()" function) far enough,
            # is if I get an AttributeError. Perhaps there is a better way of doing this, but this one seems to work.
            try:
                soup.contents
                soup.html.unwrap()
                soup.contents
                soup.body.unwrap()
                soup.contents
                soup.head.unwrap()
                soup.contents
                soup.p.unwrap()
                soup.contents
            except AttributeError:
                pass
            # I am here making use of the feauture of BeautifulSoup that originally struck me as annoying, namely that it automatically splits
            # "is a <b>bold</>ed" into ['is', 'a', <b>bold</b>, 'ed']. But I can't have that. I need <b>bold</b> and 'ed' in the same sublist.
            # So I just did soup.contents after I had already for-looped my way into the word [<b>bold</b>ed]. soup.contents of [<b>bold</b>ed]
            # is [<b>bold</b>, 'ed']. So I just set that result (syllables) to be the value of the given "word" in scannedinputbylinesbywords.
            # But: all of this ONLY if the word is multi-syllabic!
            syllables = soup.contents
            # print(f"Syllables1: {syllables}")
            syllables = [x for x in syllables if x != "."]
            syllables = [x for x in syllables if x != ","]
            syllables = [x for x in syllables if x != ";"]
            ######syllables = [x for x in syllables if x != "<head></head>"]
            
            q = soup.find_all("b")
            # print(f"q: {syllables}")
            if len(syllables) > 1:
                # Adjusting the scannedbinary list structure
                scannedbinarybylinesbywords[lineindex][wordindex] = [0 for x in range(len(syllables))]
                # print(f"muli-syllabic word found: {scannedinputbylinesbywords[lineindex][wordindex]}")
                # Adjusting the scannedinput list structure (see the above explanation of this "if len(syllables) > 1"-clause)
                scannedinputbylinesbywords[lineindex][wordindex] = soup.contents
                # Finds words with the bold ("<b></b>") tag. (In the case of tri-syllabic words, for example, there could be more than one such tag.)
                q = soup.find_all("b")
                # Okay, so let us suppose a tri-syllabic word like [<b>bold</b>, 'ed', <b>er</b>] which is not a word, but so be it.
                # What we want is [1, 0, 1].
                # q (= soup.find_all("b")) would look like this: [<b>bold</b>, <b>er</b>]
                # We want to say: for 0, then for 1 (i in the range of the length of the q-list), let p be the element at that index in q.
                for i in range(len(q)):
                    # Now, use p to find the index of that element in SYLLABLES (which, recall, is: [<b>bold</b>, 'ed', <b>er</b>]).
                    indexofboldsyllable = syllables.index(q[i])
                    # Now use THAT index, which is the index of the bold syllable in question, let the element at that index in the scannedbinary list
                    # be set equal to 1.
                    scannedbinarybylinesbywords[lineindex][wordindex][indexofboldsyllable] = 1
            else:
                # Word NOT multi-syllabic (Why do I check, then? you ask. Well, why do humans have tailbones? Atavism is the spice of life.)
                if not isinstance(word, list):
                    wordaslist = list(word)
                    if (len(q) == 1) and wordaslist[:3] == ['<', 'b', '>'] and (wordaslist[(len(wordaslist)-1) - 4:(len(wordaslist)-1)] == ['<', '/', 'b', '>'] or wordaslist[(len(wordaslist)-1) - 3:] == ['<', '/', 'b', '>']): #
                        wordlistasstring = ''.join(wordaslist)
                        scannedbinarybylinesbywords[lineindex][wordindex] = 1

    # print(f"scannedbinarybylinesbywords after loop: {scannedbinarybylinesbywords}")

    asciifileasbinarylist = []

    for x in asciifileasbinary:
        asciifileasbinarylist.append([int(i) for i in x])

    print(f"asciiasbinarylist: {asciifileasbinarylist}")

    outputlist = []
    recursiondepth = 0
    for i in asciifileasbinarylist:
        q = randomslicematch(i, scannedbinarybylinesbywords, scannedinputbylinesbywords, outputlist, recursiondepth)

    outputlist = [[str(x) if not isinstance(x, str) else x for x in y] if isinstance(y, list) else y for y in outputlist]
    # Outputlist contained certain TAGGED but not stringified words (inevitable grease from the hands of BeautifulSoup);
    # Here, look for lists, then check for non-strings in that list element and render them as strings.

    outputlist = ["".join(word) if isinstance(word, list) else word for word in outputlist]
    # print(f"outputlist: {outputlist}")
    outputlist = flatten(outputlist)
    outputasplaintext = " ".join(outputlist)

    return render_template("emphasize.html", file1=file1, file2=outputasplaintext)


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
