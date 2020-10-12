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

# inputlist: ascii as binary in list form
# databasebinary: binary representation of verse
# databaseverse: verse (html, isomorphic to databasebinary)
# outputlist: not isomorphic to anything; the structure is meaningless, except that instances of
#  nested lists should be limited to multisyllabic words.
def randomslicematch(inputlist, databasebinary, databaseverse, outputlist):
  for y in range(0, len(inputlist)):
    rand = 0
    if len(inputlist) == 0:
        return outputlist    
    if len(inputlist) > 4:
      rand = random.randrange(1, 5)
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
        return randomslicematch(inputlist, databasebinary, databaseverse, outputlist)
        # abort(400, f"no word found for ascii-as-binary slice2: {slicetobefound}")
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

    #pythoninputbychunksbylinesbykeywords = []

    ######print(f"file1: {file1}")
    #a = file1.split('\n\n\n')
    # a = file1
    # b = binascii.a2b_uu(file1)
    # b = binascii.a2b_uu('a')
    #d = "abcd"
    #b = ''.join([bin(ord(c))[2:].rjust(8,'0') for c in d])
    #print(f"experiment: {b}")
    #print(f"type: {type(b)}")
    # reconstruction = decode_binary_string(b)
    # print(f"abcd: {reconstruction}")
    #b = a.split('\\\n')
    #print(f"experiment: {a}")






    asciifileasbinary = encode_string_binary(file1)

    # b = decode_binary_string(a)
    # print(f"original&&&&&&: {b}")

    
    




                    # # Creates a list of input file containing python text, first chunk by chunk ("chunk" means a chunk of code separated
                    # # on either end by triple newlines (i.e. two empty lines between each occurence of text))
                    # # and then (nested in each chunk) line by line.

                    # pythoninputbychunksbylinesbykeywords = [x.split('\n') for x in file1.split('\n\n\n')]

                    # #pythoninputbychunksbylinesbykeywords = flatten(pythoninputbychunksbylinesbykeywords)
                    # # print(f"python by chunks: {pythoninputbychunksbylinesbykeywords}")

                    # ##pythoninputbychunksbylinesbykeywords = [[x for x in y if "{" not in x] for y in pythoninputbychunksbylinesbykeywords]
                    # #pythoninputbychunksbylinesbykeywords = [[x for x in y if "\\" not in x] for y in pythoninputbychunksbylinesbykeywords]
                    # #pythoninputbychunksbylinesbykeywords = [[','.join(x) for x in y] for y in pythoninputbychunksbylinesbykeywords]

                    # #pythoninputbychunksbylinesbykeywords = [x.split("'',''") for x in pythoninputbychunksbylinesbykeywords]
                    # #smallerlist = [l.split(',') for l in ','.join(biglist).split('|')]

                    # # Gets rid of list elements representing double newlines (i.e. one empty line), which often occur within chunks
                    # #pythoninputbychunksbylinesbykeywords = [[x for x in y if x != ""] for y in pythoninputbychunksbylinesbykeywords] # no need for "\n" just "" (see visualizer) ###### Isn't working; 0's for single-line breaks in output
                    # #######print(pythoninputbychunksbylinesbykeywords)
                    # # Creates a new list, this time for the BINARY representation of the python text original, based on the list-structure of
                    # # the original pythonINPUTbychunksbylinesbykeywords list.
                    # pythonbinarybychunksbylinesbykeywords = [[0 for x in y] for y in pythoninputbychunksbylinesbykeywords]

                    # # print(f"python binary by chunks: {pythonbinarybychunksbylinesbykeywords}")
                    # ######print(f"abc: {pythoninputbychunksbylinesbykeywords}")
                    # # Python keywords
                    # # Removed:
                    # # 'elif ' because of "if"
                    # # 'for ' because of "or"
                    # # 'not ' because always compounded with another
                    # # Changes:
                    # # ' ' added to end of all but "print", "yield", "None", "True", and "False"
                    # # 'else:' used instead of 'else '

                    # # Keywords taken from https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
                    # # Will later be used for representing different sorts of python lines with different sorts of binary lists
                    # keywords = [
                    #     'and ', 'assert ', 'break ', 'class ', 'continue ', 'def ',
                    #     'del ', 'else:', 'except ', 'exec ', 'finally ',
                    #     'from ', 'global ', 'if ', 'import ', 'in ',
                    #     'is ', 'lambda ', 'or ', 'pass ', 'print',
                    #     'raise ', 'return ', 'try ', 'while ' , 'yield',
                    #     'None', 'True', 'False',
                    #     ]

                    # # For-loop uses python keywords and "=" to determine how each line of pythoninput will by represented in pythonbinary.
                    # # Iterates through list of python text input, chunk by chunk
                    # for chunk in pythoninputbychunksbylinesbykeywords:

                    #     # Makes a list of the indexes all instances in pythoninputbychunksbylinesbykeywords of the given chunk:
                    #     chunkindices = [i for i, x in enumerate(pythoninputbychunksbylinesbykeywords) if x == chunk]

                    #     # Goes to line in python chunk (e.g. "for x in y:" or "p = q")
                    #     for line in chunk:

                    #         # Makes a list of the indexes of all instances in the given chunk of the given line:
                    #         lineindices = [i for i, x in enumerate(pythoninputbychunksbylinesbykeywords[chunkindices[0]]) if x == line]

                    #         # Stores in "q2" all the "keywords" found in the given line
                    #         # but ultimately the "q" list will only be used to checks HOW MANY instances of the keywords occur in the given line
                    #         q2 = [re.findall(x, line) for x in keywords if re.findall(x, line) != []]

                    #         # Flattens q2
                    #         q3 = flatten(q2)

                    #         # If there is one keyword, replace the corresponding element in the BINARY list (which element is currently "0") with "[1, 0]"
                    #         # (this effectively links it to a two-syllable word, which will also be represented in binary with a two-element sublist)
                    #         # Example: ['if y > 0:', 'import re'] in pythoninputbychunksbylinesbykeywords,
                    #         # which was originally represented as [0, 0] in pythonbinarybychunksbylinesbykeywords,
                    #         # now becomes [[1, 0], [1, 0]] in pythonbinarybychunksbylinesbykeywords.
                    #         if (len(q3)) == 1:
                    #             # Indexes into all instances of the chunk/line
                    #             for chunkindex in chunkindices:
                    #                 for lineindex in lineindices:
                    #                     # Note that this is now pythonBINARYbychunksbylinesbykeywords (which, recall, has a list-structure that is identical
                    #                     # to pythonINPUTbychunksbylinesbykeywords)
                    #                     pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [1, 0]

                    #         # Same sort of thing here, except for input lines like ['if x in y:'] (as both "if" and "in" are in the keywords list)
                    #         # or ['from x import y'] ("from" and "import" being the two keywords, here)
                    #         elif (len(q3)) == 2:
                    #             #options = [[0, 1, 0], [1, 0, 1]]
                    #             # added (double for-loops):
                    #             for chunkindex in chunkindices:
                    #                 for lineindex in lineindices:
                    #                     pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1] # line was previously: 0; now it is: [0, 1, 0, 1]; now [1, 0, 1]; no [1, 0]; back to [0, 1, 0, 1]

                    #         # Again (rarer; usually list-comprehensions, I think)
                    #         elif (len(q3)) == 3:
                    #             for chunkindex in chunkindices:
                    #                 for lineindex in lineindices:
                    #                     # Alternates for 3-keyword lines
                    #                     if (lineindices.index(lineindex) % 2) == 0:
                    #                         pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [1, 0, 1]
                    #                     else:
                    #                         pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1, 0]
                    #                         # ((a rogue 1 on line 30 of "test repeat"))

                    #         # Need I say more?
                    #         elif (len(q3)) == 4:
                    #             for chunkindex in chunkindices:
                    #                 for lineindex in lineindices:
                    #                     pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1, 0, 1]

                    #         # Input lines like ['p = q']
                    #         elif "=" in line:
                    #             for chunkindex in chunkindices:
                    #                 for lineindex in lineindices:
                    #                     pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = 1

                    # print(f"pythoninputbychunksbylinesbykeywords: {pythoninputbychunksbylinesbykeywords}")
                    # print(f"pythonbinarybychunksbylinesbykeywords: {pythonbinarybychunksbylinesbykeywords}")



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

    print(f"scannedinputbylinesbywords: {scannedinputbylinesbywords}")


    # Creates binary list that is, so to speak, isomorphic to the list of the words of the original (following the floating-tag-reformatting above)
    # (Same thing as was done for the pythonbinary___ list-creation from the pythoninput___ original, above.)
    scannedbinarybylinesbywords = [[0 for x in y] for y in scannedinputbylinesbywords]
    print(f"scannedbinarybylinesbywords before loop: {scannedbinarybylinesbywords}")

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
            print(f"Syllables1: {syllables}")
            syllables = [x for x in syllables if x != "."]
            syllables = [x for x in syllables if x != ","]
            syllables = [x for x in syllables if x != ";"]
            ######syllables = [x for x in syllables if x != "<head></head>"]
            print(f"Syllables2: {syllables}")
            # head = syllables.find_all("head")
            # print(f"head tag: {head}")
            #syllables [x for x in syllables if x !=]
            q = soup.find_all("b")
            print(f"q: {syllables}")
            if len(syllables) > 1:
                # Adjusting the scannedbinary list structure
                scannedbinarybylinesbywords[lineindex][wordindex] = [0 for x in range(len(syllables))]
                print(f"muli-syllabic word found: {scannedinputbylinesbywords[lineindex][wordindex]}")
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

    print(f"scannedbinarybylinesbywords after loop: {scannedbinarybylinesbywords}")


    ###### Speaking of atavism, I am leaving this chunk of code here, NOT accidentally, but as a monument to the rare relation existing between
    ###### (1) the amount time I poured into it; (2) the extent to which it not only is useless but also in fact detracts from the output (insofar
    ###### (as I should have forseen) as it limits the VARIETY of the output for any given chunk of python code); and (3) the significance of (2).
    ###### Indeed, (2) —— i.e. the fact of its dead weight —— could be said to vindicate my entire conception of the matter.
    ###### What did this code do? It found the verseline that was MOST SIMILAR to the given python chunk, then prioritized selection of python elements
    ###### from that verseline.
    # outputlistbylines = []
    # for pythonchunk in pythonbinarybychunksbylinesbykeywords:
    #     if pythonchunk in scannedbinarybylinesbywords:
    #         print("Chunk is in line!")
    #         verselineindex = scannedbinarybylinesbywords.index(pythonchunk)
    #         pythonchunkasverseline = scannedinputbylinesbywords[verselineindex]
    #         outputlistbylines.append(pythonchunkasverseline)
    #     else:
    #         pythonchunkindex = pythonbinarybychunksbylinesbykeywords.index(pythonchunk)
    #         print(f"pythonchunkindex:", pythonchunkindex)
    #         chunkelementsindicesofincidence = []
    #         print(f"for pythonchunk {pythonchunk}")
    #         for pythonline in pythonchunk:
    #             indicesofincidence = []
    #             chunkelementsindicesofincidence.append(indicesofincidence)
    #             for verseline in scannedbinarybylinesbywords:
    #                 if pythonline in verseline:
    #                     listofduplicates = list_duplicates_of(verseline, pythonline)
    #                     if len(listofduplicates) == 1:
    #                         indicesofincidence.append(verseline.index(pythonline))
    #                     else:
    #                         indicesofincidence.append(listofduplicates)
    #                 else:
    #                     indicesofincidence.append(0)
    #         checksperelement = len(scannedbinarybylinesbywords)
    #         rating = 0
    #         scannedbinarylinesrated = {}
    #         for verseline in scannedbinarybylinesbywords:
    #             verselineasstring = str(verseline)
    #             scannedbinarylinesrated[verselineasstring] = 0 ###### A problem: https://stackoverflow.com/questions/10664856/make-dictionary-with-duplicate-keys-in-python
    #         for i in range(len(chunkelementsindicesofincidence) - 1, 0, -1): # start from end, iterate down
    #             for j in range(checksperelement - 1, -1, -1): ###### why not end at 0?
    #                 elementjthlist = chunkelementsindicesofincidence[i][j]
    #                 prevelementjthlist = chunkelementsindicesofincidence[i-1][j]
    #                 if type(elementjthlist) is list and type(prevelementjthlist) is list:
    #                     for subincidence in elementjthlist:
    #                         for prevsubincidence in prevelementjthlist:
    #                             if subincidence - prevsubincidence == 1:
    #                                 chunkelementsindicesofincidence[i][j] = subincidence
    #                                 chunkelementsindicesofincidence[i-1][j] = prevsubincidence
    #                                 break
    #                     else:
    #                         chunkelementsindicesofincidence[i][j] = subincidence
    #                         chunkelementsindicesofincidence[i-1][j] = prevsubincidence
    #                 elif type(elementjthlist) is list:
    #                     for subincidence in elementjthlist:
    #                         if subincidence - prevelementjthlist == 1:
    #                             chunkelementsindicesofincidence[i][j] = subincidence
    #                             break
    #                     else:
    #                         chunkelementsindicesofincidence[i][j] = subincidence
    #                 elif type(prevelementjthlist) is list:
    #                     for prevsubincidence in prevelementjthlist:
    #                         if elementjthlist - prevsubincidence == 1:
    #                             chunkelementsindicesofincidence[i-1][j] = prevsubincidence
    #                             break
    #                     else:
    #                         chunkelementsindicesofincidence[i-1][j] = prevsubincidence
    #                 if (chunkelementsindicesofincidence[i][j] - chunkelementsindicesofincidence[i-1][j]) == 1:
    #                     verselineas = str(scannedbinarybylinesbywords[j])
    #                     scannedbinarylinesrated[verselineas] += 1
    #         # print(f"chunkelementsindicesofincidence {chunkelementsindicesofincidence}")
    #         # verseline_binary_as_key_string_to_be_searched = max(scannedbinarylinesrated.items(), key=operator.itemgetter(1))[0] ######
    #         # print(f"max values {max(scannedbinarylinesrated.items(), key=operator.itemgetter(1))}")
    #         # verseline_binary_as_list_to_be_searched = ast.literal_eval(verseline_binary_as_key_string_to_be_searched)

    #         # verselineindex = scannedbinarybylinesbywords.index(verseline_binary_as_list_to_be_searched)

    #         #for pythonline in pythonbinarybychunksbylinesbykeywords[pythonchunkindex]:
    #         sorted_scannedbinarylinesrated = sorted(scannedbinarylinesrated.items(), key=operator.itemgetter(1))
    #         #scannedbinarylinesrated_as_sorted_dict = dict(sorted_scannedbinarylinesrated)
    #         #print(f"scannedbinarylinesrated as sorted dict: {scannedbinarylinesrated_as_sorted_dict}")
    #         #print(f"max values {max(scannedbinarylinesrated.items(), key=operator.itemgetter(1))}")
    #         print(f"scannedbinarylinesrated as sorted tuples: {sorted_scannedbinarylinesrated}")

    #         #for i in range(len(max(scannedbinarylinesrated.items(), key=operator.itemgetter(1)))):

    #         verselineindex = 0

    #         for i in range((len(sorted_scannedbinarylinesrated) - 1), -1, -1):
    #             print(f"i: {i}")
    #             #verseline_binary_as_key_string_to_be_searched = max(scannedbinarylinesrated.items(), key=operator.itemgetter(1))[i]
    #             #verseline_binary_as_key_string_to_be_searched = scannedbinarylinesrated_as_sorted_dict[i]
    #             verseline_binary_as_key_string_to_be_searched = sorted_scannedbinarylinesrated[i][0]
    #             print(f"verseline_binary_as_key_string_to_be_searched (last to first): {verseline_binary_as_key_string_to_be_searched}")
    #             verseline_binary_as_list_to_be_searched = ast.literal_eval(verseline_binary_as_key_string_to_be_searched)
    #             verselineindex = scannedbinarybylinesbywords.index(verseline_binary_as_list_to_be_searched)
    #             #print(f"")
    #             # The pythonlines get repeated if there is a break following successful appendings; that is, the "pythonline in pythonchunk"
    #             # loop restarts after a break, even if the first few pythonlines WERE in scannedbinarybylinesbywords[verselineindex].
    #             # We want to check every pythonline FIRST, but we also want the second loop (for appending), to occur only
    #             if i == -1:
    #                 print("NO MATCHES")
    #             for pythonline in pythonchunk:
    #                 print(f"pythonline: {pythonline}")
    #                 if pythonline not in scannedbinarybylinesbywords[verselineindex]:
    #                     print("Breaking!")
    #                     break
    #             else:
    #                 break

    #         print("This verseline got through (you should NOT see Breaking! just before this)")
    #         for pythonline in pythonchunk:
    #             randomindexinverseline = random.randrange(0, len(scannedbinarybylinesbywords[verselineindex]))
    #             while pythonline != scannedbinarybylinesbywords[verselineindex][randomindexinverseline]:
    #                 randomindexinverseline = random.randrange(0, len(scannedbinarybylinesbywords[verselineindex]))
    #             pythonlineasverseword = scannedinputbylinesbywords[verselineindex][randomindexinverseline]
    #             outputlistbylines.append(pythonlineasverseword)
    ######

    # Instead we look for matches by, as it were, random choice. The timeout clause in the while loop
    # executes in cases in which there is a pythonlinebinary element that cannot find a corresponding verselinebinary element,
    # as would often be the case if you had a pythonline with four or more keywords in it, as that would be represented as [0, 1, 0, 1].
    # So, unless the scannedinput has a four-syllable word, it would be unlikely that that pythonline would find a match.
    # ((Perhaps I will get rid of the if len(q3) > 4: --> [0, 1, 0, 1] assignment, if I find this is too common.))
    
    
    
    #asciifileasbinary
    asciifileasbinarylist = list(asciifileasbinary)
    outputlist = []
    outputlist = randomslicematch(asciifileasbinarylist, scannedbinarybylinesbywords, scannedinputbylinesbywords, outputlist)
    


                    # for pythonchunk in pythonbinarybychunksbylinesbykeywords:
                    #     for pythonline in pythonchunk:
                    #         randomverselineindex = random.randrange(0, len(scannedbinarybylinesbywords))
                    #         randomindexinverseline = random.randrange(0, len(scannedbinarybylinesbywords[randomverselineindex]))
                    #         timeout = time.time() + 6
                    #         while pythonline != scannedbinarybylinesbywords[randomverselineindex][randomindexinverseline]:
                    #             randomverselineindex = random.randrange(0, len(scannedbinarybylinesbywords))
                    #             randomindexinverseline = random.randrange(0, len(scannedbinarybylinesbywords[randomverselineindex]))
                    #             if time.time() > timeout:
                    #                 abort(400, f"no word found for pythonline {pythonline}")
                    #         pythonlineasverseword = scannedinputbylinesbywords[randomverselineindex][randomindexinverseline]
                    #         outputlistbylines.append(pythonlineasverseword)

    # Outputlist contained certain TAGGED but not stringified words (inevitable grease from the hands of BeautifulSoup);
    # Here, look for lists, then check for non-strings in that list element and render them as strings.
    outputlist = [[str(x) if not isinstance(x, str) else x for x in y] if isinstance(y, list) else y for y in outputlist]

    # Now we join the outputlist multi-syllabic words, else word for word... Wait, isn't this effectively flattening the outputlist? So then
    # could I have just done this "joining" business instead of making my absurd flatten function??
    outputlist = ["".join(word) if isinstance(word, list) else word for word in outputlist]

    # Join astride spaces. (This gives output some extra whitespace in places.)
    outputasplaintext = " ".join(outputlist)

    return render_template("emphasize.html", file1=file1, file2=outputasplaintext)


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
