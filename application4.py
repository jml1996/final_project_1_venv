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


@app.route("/compare", methods=["POST"])
def compare():
    """Handle requests for /compare via POST"""

    # Read files
    if not request.files["file1"] or not request.files["file2"]:
        abort(400, "missing file")
    try:
        file1 = request.files["file1"].read().decode("utf-8")
        file2 = request.files["file2"].read().decode("utf-8")
    except Exception:
        abort(400, "invalid file")

    # chunks == lines; lines == words; keyword-clauses == syllables (in multisyllabic words)

    # Code (down to end of "chunk" loop) original file: python_keyword.py


    pythoninputbychunksbylinesbykeywords = []

    # Creates a list of input file containing python text, first chunk by chunk ("chunk" means a chunk of code separated
    # on either end by triple newlines (i.e. two empty lines between each occurence of text))
    # and then (nested in each chunk) line by line.
    pythoninputbychunksbylinesbykeywords = [x.split('\n') for x in file1.split('\n\n\n')]

    # Gets rid of list elements representing double newlines (i.e. one empty line), which often occur within chunks
    pythoninputbychunksbylinesbykeywords = [[x for x in y if x != ""] for y in pythoninputbychunksbylinesbykeywords] # no need for "\n" just "" (see visualizer) ###### Isn't working; 0's for single-line breaks in output

    # Creates a new list, this time for the BINARY representation of the python text original, based on the list-structure of
    # the original pythonINPUTbychunksbylinesbykeywords list.
    pythonbinarybychunksbylinesbykeywords = [[0 for x in y] for y in pythoninputbychunksbylinesbykeywords]

    # Python keywords
    # Removed:
    # 'elif ' because of "if"
    # 'for ' because of "or"
    # 'not ' because always compounded with another
    # Changes:
    # ' ' added to end of all but "print", "yield", "None", "True", and "False"
    # 'else:' used instead of 'else '

    # Keywords taken from https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
    # Will later be used for representing different sorts of python lines with different sorts of binary lists
    keywords = [
        'and ', 'assert ', 'break ', 'class ', 'continue ', 'def ',
        'del ', 'else:', 'except ', 'exec ', 'finally ',
        'from ', 'global ', 'if ', 'import ', 'in ',
        'is ', 'lambda ', 'or ', 'pass ', 'print',
        'raise ', 'return ', 'try ', 'while ' , 'yield',
        'None', 'True', 'False',
        ]

    # For-loop uses python keywords and "=" to determine how each line of pythoninput will by represented in pythonbinary.
    # Iterates through list of python text input, chunk by chunk
    for chunk in pythoninputbychunksbylinesbykeywords:
        # Notes index of each chunk, as this will be used later ((probably there would be ways to omit this "manual" indexing, but it seems to work))
        chunkindex = pythoninputbychunksbylinesbykeywords.index(chunk)
        # Goes to line in python chunk (e.g. "for x in y:" or "p = q")
        for line in chunk:
            # Notes line index
            lineindex = pythoninputbychunksbylinesbykeywords[chunkindex].index(line)
            # This little "for x in keywords" loop technically stores in "q" all the "keywords" found in the given line
            # but ultimately the "q" list will only be used to checks HOW MANY instances of the keywords occur in the given line
            q = []
            for x in keywords:
                if re.findall(x, line) != []:
                    q.append(x)
            # If there is one keyword, replace the corresponding element in the BINARY list (which element is currently "0") with "[0, 1]"
            # (this effectively links it to a two-syllable word, which will also be represented in binary with a two-element sublist)
            # Example: ['if y > 0:', 'import re'] in pythoninputbychunksbylinesbykeywords,
            # which was originally represented as [0, 0] in pythonbinarybychunksbylinesbykeywords,
            # now becomes [[0, 1], [0, 1]] in pythonbinarybychunksbylinesbykeywords.
            if (len(q)) == 1:
                pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1]
            # Same sort of thing here, except for input lines like ['if x in y:'] (as both "if" and "in" are in the keywords list)
            # (this effectively links these statements to four-syllable words; obviously I will have to make changes about this sort of detail)
            elif (len(q)) == 2:
                pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1, 0, 1] # line was previously: 0; now it is: [0, 1, 0, 1]
            # Input lines like ['p = q']
            elif "=" in line:
                pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = 1


    # Code (down to end of "line" loop) original file: spilt_whitespace.py


    # New list for scanned input. List structured first by the html "<div>" tag... hmm...
    # I changed it to the combination of "</p><p>", because these seem to be how line breaks are tagged in html...
    # I should say: the way I am testing this is with two .rtf (textEdit) files: file1 is the python test code, file2 is the html rendition of a
    # .docx file containing the verse text original (in which "bolded" words or syllables represent STRESSED words or syllables).
    # To get this html version, I simply copy-and-pasted the .docx text into an online word-to-html converter. I then pasted the output
    # from this converter into that .rtf file which I uploaded as file2.
    # I will at some point need to come up with a method of automating this conversion from word-doc (or pdf) originals to html.
    # (Taking a step back, I want it in html, because with an html string I can work with both tags and whitespace, whereas with .docx
    # text I can only work with runs (see https://msdn.microsoft.com/en-us/library/office/gg278312.aspx). Moreover, conversion to html seems
    # to maintain, with zero or negligible error, bolded text from the .docx files and label it with the <b></b> tag.)
    # The value I will use for this "file2.split(______)" will depend on how I automate the conversion of .docx (or .pdf or .rtf) text to .html text,
    # as it seems that different converters convert newlines differently. (I was, e.g., using "</div>" instead of "</p>" in a test program.)
    scannedinputbylinesbywords = [x.split() for x in file2.split("</p>")]

    # Reformats floating "</b>" tags (as in: ['this', '<b>is', '</b>', 'a']) (due to whitespace split).
    # And did same for "<b>" tags (even though bolded whitespace seems only to occur in the whitespace between the text and the TRAILING </b> tag).
    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line)
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word)
            if word == "</b>":
                # Literally pastes the </b> end-tag onto the end of the preceding word, and deletes the list-element that was previously occupied
                # by the </b> end-tag.
                q = scannedinputbylinesbywords[lineindex][wordindex - 1]
                scannedinputbylinesbywords[lineindex][wordindex - 1] = q + "</b>"
                scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])
            elif word == "<b>":
                q = scannedinputbylinesbywords[lineindex][wordindex + 1]
                scannedinputbylinesbywords[lineindex][wordindex + 1] = "<b>" + q
                scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])

    # Creates binary list that is, so to speak, isomorphic to the list of the words of the original (following the floating-tag-reformatting above)
    # (Same thing as was done for the pythonbinary___ list-creation from the pythoninput___ original, above.)
    scannedbinarybylinesbywords = [[0 for x in y] for y in scannedinputbylinesbywords]

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
    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line)
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word)
            soup = BeautifulSoup(''.join(word))
            # This "try-except" method came about because I want to strip the word down until it is of the form '<b>This</b>' or 'is,'
            # but the only way I know I have stripped it down (which I do with BeautifulSoup's "unwrap()" function) far enough,
            # is if I get an AttributeError. Perhaps there is a better way of doing this, but this one seems to work.
            try:
                soup.contents
                soup.html.unwrap()
                soup.contents
                soup.body.unwrap()
                soup.contents
            except AttributeError:
                pass
            # I am here making use of the feauture of BeautifulSoup that originally struck me as annoying, namely that it automatically splits
            # "is a <b>bold</>ed" into ['is', 'a', <b>bold</b>, 'ed']. But I can't have that. I need <b>bold</b> and 'ed' in the same sublist.
            # So I just did soup.contents after I had already for-looped my way into the word [<b>bold</b>ed]. soup.contents of [<b>bold</b>ed]
            # is [<b>bold</b>, 'ed']. So I just set that result (syllables) to be the value of the given "word" in scannedinputbylinesbywords.
            # But: all of this ONLY if the word is multi-syllabic!
            syllables = soup.contents
            if len(syllables) > 1:
                # Adjusting the scannedbinary list structure
                scannedbinarybylinesbywords[lineindex][wordindex] = [0 for x in range(len(syllables))]
                # Adjusting the scannedinput list structure (see the above explanation of this "if len(syllables) > 1"-clause)
                scannedinputbylinesbywords[lineindex][wordindex] = soup.contents
                # Finds words with the bold ("<b></b>") tag. (In the case of tri-syllabic words, for example, there could be more than one such tag.)
                q = soup.find_all("b")
                # Okay, so let us suppose a tri-syllabic word like [<b>bold</b>, 'ed', <b>er</b>] which is not a word, but so be it.
                # What we want is [1, 0, 1].
                # q (= soup.find_all("b")) would look like this: [<b>bold</b>, <b>er</b>]
                # We want to say: for 0, then for 1 (i in the range of the length of the q-list), let p be the element at that index in q.
                for i in range(len(q)):
                    p = q[i]
                    # Now, use p to find the index of that element in SYLLABLES (which, recall, is: [<b>bold</b>, 'ed', <b>er</b>]).
                    indexofboldsyllable = syllables.index(p)
                    # Now use THAT index, which is the index of the bold syllable in question, let the element at that index in the scannedbinary list
                    # be set equal to 1.
                    scannedbinarybylinesbywords[lineindex][wordindex][indexofboldsyllable] = 1
            # Otherwise, it's a single-syllabic word and you can just check for the <b> and </b> tags, with the option of trailing whitespace for
            # the latter.
            elif "<b>" and ("</b>" or " </b>") in word:
                scannedbinarybylinesbywords[lineindex][wordindex] = 1

    # Each output "verse" line should represent one chunk of python code.
    outputlistbylines = []

    # Alright. Strap in. This is where it starts to get interesting.
    # This for-loop calls for the function findmatch, which takes four arguments: (1) the chunk of python binary ([1, 0, 1], say) to be matched
    # with some item in...; (2) the scannedbinary list, the indices of which will indicate the corresponding words in...; (3) the scannedinput
    # list, which will then print those to...; (4) chunkasline, which is a list representing a line
    # and which consists of scanned words, like [<b>bold</b>, 'ed', <b>ed</b>].
    # Unfortunately, the findmatch function is recursive and throws a "max recursive depth limit reached" error.

    # I have made some slight changes to the below for-loop. (1) I included a second "for line in scannedbinarybylinesbywords," so that each line
    # would be recursively tested....
    chunkasline = []
    for chunk in pythonbinarybychunksbylinesbykeywords:
        if chunk in scannedbinarybylinesbywords:
            verselineindex = scannedbinarybylinesbywords.index(chunk)
            pythonchunkasverseline = scannedinputbylinesbywords[verselineindex]
        #for line in scannedbinarybylinesbywords: ######
            #lineindex = scannedbinarybylinesbywords.index(line) ######
            #scannedline = scannedinputbylinesbywords[lineindex] ######
            #pythonchunkasverseline = findmatch(chunk, line, scannedline, chunkasline) ######
        else:
            pythonchunkasverseline = findmatch(chunk, scannedbinarybylinesbywords, scannedinputbylinesbywords, chunkasline)
        outputlistbylines.append(pythonchunkasverseline)

    return render_template("compare.html", file1=file1, file2=outputlistbylines)

# As of 11/30/17 at 8:17 PM: def findmatch(chunk, scannedbinarybylinesbywords == list2, scannedinputbylinesbywords == languagemodelledbylist2, chunkasline)

def findmatch(chunk, list2, languagemodelledbylist2, chunkasline):
    # If there is an IDENTICAL match for the whole chunk (a sublist) of python-qua-binary, in the verse-qua-binary
    # list —— remember, chunk IS the sublist, not an index.
    # This is in some sense the base case, because, given that we are working with 1's and 0's, there will always be a match here eventually...
    random.shuffle(list2)
    for line in list2: ###### randomize
        verselineindex = list2.index(line)
        if search(line, chunk) != -1:
            #scannedwordindex = list2[verselineindex].index(chunk)
            #scannedwordindex = search(line, chunk)
            startofoverlapflat = search(line, chunk)

            # startofoverlap = deflatten ___startofoverlapflat___ ######
            # endofoverlap = startofoverlap + len(chunk) ######

            # Appends the language (scannedinput) modelled by list2 (scannedbinary) at the index corresponding to the match of the chunk.
            chunkasline.append(languagemodelledbylist2[verselineindex][startofoverlap:endofoverlap])
        # Otherise, if the chunk is not in list2, split it into two parts and run findmatch with both of those split-chunks as the new chunk.
        # So if your original chunk was [1, 0, 1], now you have [1] and [0, 1].
        else:
            splitpoint = int(math.floor(len(chunk)/2))
            findmatch(chunk[:splitpoint], list2, languagemodelledbylist2, chunkasline)
            findmatch(chunk[splitpoint:], list2, languagemodelledbylist2, chunkasline)
            # can you run two refcursions simultaneously?
    return chunkasline


# this is insane
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


# https://stackoverflow.com/questions/3313590/check-for-presence-of-a-sliced-list-in-python
def search(haystack, needle):
    """
    Search list `haystack` for sublist `needle`.
    """
    needle = flatten(needle)
    haystack = flatten(haystack)

    if len(needle) == 0:
        return 0
    char_table = make_char_table(needle)
    offset_table = make_offset_table(needle)
    i = len(needle) - 1
    while i < len(haystack):
        j = len(needle) - 1
        while needle[j] == haystack[i]:
            if j == 0:
                return i
            i -= 1
            j -= 1
        # These next three lines were, incomprehensibly, necessary. I do not understand why char_table.get(haystack[i]) == None, when haystack[i]==0
        q = char_table.get(haystack[i])
        if char_table.get(haystack[i]) == None:
            q = 0
        i += max(offset_table[len(needle) - 1 - j], q); #";"?
    return -1


def make_char_table(needle):
    """
    Makes the jump table based on the mismatched character information.
    """
    needle = flatten(needle)
    table = {}
    for i in range(len(needle) - 1):
        #needle[i]
        table[needle[i]] = len(needle) - 1 - i
    return table

def make_offset_table(needle):
    """
    Makes the jump table based on the scan offset in which mismatch occurs.
    """
    needle = flatten(needle)
    table = []
    last_prefix_position = len(needle)
    for i in reversed(range(len(needle))):
        if is_prefix(needle, i + 1):
            last_prefix_position = i + 1
        table.append(last_prefix_position - i + len(needle) - 1)
    for i in range(len(needle) - 1):
        slen = suffix_length(needle, i)
        table[slen] = len(needle) - 1 - i + slen
    return table

def is_prefix(needle, p):
    """
    Is needle[p:end] a prefix of needle?
    """
    needle = flatten(needle)
    j = 0
    for i in range(p, len(needle)):
        if needle[i] != needle[j]:
            return 0
        j += 1
    return 1

def suffix_length(needle, p):
    """
    Returns the maximum length of the substring ending at p that is a suffix.
    """
    needle = flatten(needle)
    length = 0;
    j = len(needle) - 1
    for i in reversed(range(p + 1)):
        if needle[i] == needle[j]:
            length += 1
        else:
            break
        j -= 1
    return length










#     for chunk in pythonbinarybychunksbylinesbykeywords:
#         #for line in scannedbinarybylinesbywords: ######
#             #lineindex = scannedbinarybylinesbywords.index(line) ######
#         chunkasline = []
#         pythonchunkasverseline = findmatch(chunk, scannedbinarybylinesbywords, scannedinputbylinesbywords, chunkasline)
#             #scannedline = scannedinputbylinesbywords[lineindex] ######
#             #pythonchunkasverseline = findmatch(chunk, line, scannedline, chunkasline)
#         outputlistbylines.append(pythonchunkasverseline)

#     return render_template("compare.html", file1=file1, file2=outputlistbylines)

# # As of 11/30/17 at 8:17 PM: def findmatch(chunk, scannedbinarybylinesbywords == list2, scannedinputbylinesbywords == languagemodelledbylist2, chunkasline)

# def findmatch(chunk, list2,  languagemodelledbylist2, chunkasline):
#     # If there is an IDENTICAL match for the whole chunk (a sublist) of python-qua-binary, in the verse-qua-binary
#     # list —— remember, chunk IS the sublist, not an index.
#     # This is in some sense the base case, because, given that we are working with 1's and 0's, there will always be a match here eventually...
#     for line in list2:
#         if chunk in line:
#             verselineindex = list2.index(chunk)
#             chunkasline.append(languagemodelledbylist2[verselineindex])

#     for pythonlinebinary in chunk:
#         for scannedbinaryline in list2:
#             lineindex = list2.index(scannedbinaryline)
#             scannedline = languagemodelledbylist2[lineindex]
#             if pythonlinebinary in scannedbinaryline:
#                 versewordindex = list2[lineindex].index(pythonlinebinary)
#                 # Appends the language (scannedinput) modelled by list2 (scannedbinary) at the index corresponding to the match of the chunk.
#                 chunkasline.append(languagemodelledbylist2[lineindex][w])
#             # Otherise, if the chunk is not in list2, split it into two parts and run findmatch with both of those split-chunks as the new chunk.
#             # So if your original chunk was [1, 0, 1], now you have [1] and [0, 1].
#             else:
#                 splitpoint = int(math.floor(len(chunk)/2))
#                 findmatch(chunk[:splitpoint], list2, languagemodelledbylist2, chunkasline)
#                 findmatch(chunk[splitpoint:], list2, languagemodelledbylist2, chunkasline)
#                 # can you run two recursions simultaneously?
#     return chunkasline


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
