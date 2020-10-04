import re
from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
from docx import *
import math

from helpers import lines, sentences, substrings

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

###### Problems:
###### (1) [1, 0] finds [1] and [0] before the first two elements of [1, 0, 1]
###### (2) it is not really word-by-word. What needs to happen is for each word to be checked for bolded AND unbolded text, then for the ORDERING
###### of that bold/unbold to determine whether the word is given a 1-token (1 syllable; 1 or 0), 2-token (2 syllable;
###### [1, 0], [0, 1], [0, 0], [1, 1]), etc., value.
###### this leads to the problem (is it a problem?) of three nested-layers in the scanned vs. 2 in the python.

    pythoninputbychunksbylines = []

    # nested list, split first around the chunks (two blank lines) (which will be equivalent to lines of verse), then around lines (words of verse)
    pythoninputbychunksbylines = [x.split('\n') for x in file1.split('\n\n\n')]

    # going from [['a'], ['xyz', '\n', 'pdq']] to [['a'], ['xyz', 'pdq']]?
    pythoninputbychunksbylines = [[x for x in y if x != "\n"] for y in pythoninputbychunksbylines]

    # duplicating pythoninputbychunksbylines (maintaining the nested structure), but replacing all values with '0', thus allowing for us only to
    # cont'd: have to make a change to the lists in the case of a 1, that is, in the case of an indentation (see the for loop below)
    # cont'd: ("\n"s already removed)
    pythonbinarybychunksbylines = [[0 for x in y] for y in pythoninputbychunksbylines]

    for chunk in pythoninputbychunksbylines:
        chunkindex = pythoninputbychunksbylines.index(chunk) # ADDED: identifies location of chunk within the whole input
        for line in chunk[1:]:
            lineindex = pythoninputbychunksbylines[chunkindex].index(line) # ADDED: identifies location of line within the chunk
            tabnumber = line.count("\t")
            tabnumberprevious = pythoninputbychunksbylines[chunkindex][lineindex - 1].count("\t") ###### FIXED (with chunkindex/lineindex): # is this "line - 1" allowed? # THESE ARE NOT INDICES; you need to find exact index of the line and word
            if tabnumber > tabnumberprevious:
                pythonbinarybychunksbylines[chunkindex][lineindex] = 1 ###### FIXED (with chunkindex/lineindex): # THESE ARE NOT INDICES; you need to find exact index of the line and word


    scannedinputbylinesbywords = [x.split() for x in file2.split("\n")]
    ## I will probably want to remove things from the scannedinput at some point, so I'm going to leave this here for now:
    # scannedinputbylinesbywords = [[x for x in y if x != "______"] for y in scannedinputbylinesbywords]

    scannedbinarybylinesbywords = [[0 for x in y] for y in scannedinputbylinesbywords]

    # I could actually probably do this whole for loop during the binary list creation above
    # con't: something like this: [[1 for x in y if x.bold else 0 ((for x in y))] for y in scannedinputbylinesbywords]
    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line) # ADDED: identifies location of line within entire input verse list
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word) # ADDED: identifies location of word within line list
            if word.bold:
                scannedbinarybylinesbywords[lineindex][wordindex] = 1 ###### THESE ARE NOT INDICES; you need to find exact index of the line and word

    # Getting bolded text: https://stackoverflow.com/questions/27904470/checking-for-particular-style-using-python-docx
    # uses "from docx import *"


    # for each chunk in pythonbinarybychunksbylines... [1, 0, 1]... check if there exists a line in scannedbinarybylinesbywords... [1, 0, 1]...
    # that is identical...
    # if so, use that line in scannedINPUTbylinesbywords as the corresponding line of the output file (still to be made).
    # if not, take the line most similar to it and edit that line by means of the line that is SECOND most similar to it (i.e. using the words
    # corresponding to (random?) 1s and 0s of second-most similar line)
    # No...
    # if NOT, pop off the last character and check for a match of this substring, then look at the popped-off characters and do the same process
    # on that list of them... i.e. [1, 0, 0, 1, 0, 0, 0], if not found, you split the list after the (i-1)th value [1, 0, 0, 1, 0, 0]
    # and check for that; if not, check for [1, 0, 0, 1, 0]; if found, check now for [0, 0]

    outputlistbylinesbywords = []
    # outputlistbylinesbywords = [[x for x in y] for y in pythoninputbychunksbylines]

#    # check for chunk in function below



    # list(set(asentences).intersection(bsentences))

    # # Compare files
    # if not request.form.get("algorithm"):
    #     abort(400, "missing algorithm")
    # elif request.form.get("algorithm") == "lines":
    #     regexes = [f"^{re.escape(match)}$" for match in lines(file1, file2)]
    # elif request.form.get("algorithm") == "sentences":
    #     regexes = [re.escape(match) for match in sentences(file1, file2)]
    # elif request.form.get("algorithm") == "substrings":
    #     if not request.form.get("length"):
    #         abort(400, "missing length")
    #     elif not int(request.form.get("length")) > 0:
    #         abort(400, "invalid length")
    #     regexes = [re.escape(match) for match in substrings(
    #         file1, file2, int(request.form.get("length")))]
    # else:
    #     abort(400, "invalid algorithm")

    outputlistbylines = []

    for chunk in pythonbinarybychunksbylines:
        chunkoutputlistbylines = [] # I do this and include it as a fourth argument because otherwise (if I included it in the body of the findmatch function/class) a new list would get created for each recursion
        pythonchunkasverseline = findmatch(chunk, scannedbinarybylinesbywords, scannedinputbylinesbywords, chunkoutputlistbylines)
        outputlistbylines.append(pythonchunkasverseline)











    # Highlight files

    highlights1 = highlight(file1, regexes)
    highlights2 = highlight(file2, regexes)

    # Output comparison
    return render_template("compare.html", file1=highlights1, file2=highlights2)

# pythonbinarybychunksbylines == list1, scannedbinarybylinesbywords == list2, scannedinputbylinesbywords == languagemodelledbylist2
# chunk, scannedbinarybylinesbywords == list2, scannedinputbylinesbywords == languagemodelledbylist2
# def findmatch(chunk, scannedbinarybylinesbywords == list2, scannedinputbylinesbywords == languagemodelledbylist2)
# As of 11/30/17 at 8:17 PM: def findmatch(chunk, scannedbinarybylinesbywords == list2, scannedinputbylinesbywords == languagemodelledbylist2, chunkoutputlistbylines)
###### add in FIFTH argument, a counter, which indicates the len(chunk); base case is thus: if counter == 1;
###### no need for a fifth argument; just need to check len(chunk) at beginning
######
def findmatch(chunk, list2,  languagemodelledbylist2, chunkoutputlistbylines):
    if chunk in list2: # IF there is an IDENTICAL match for the whole chunk (a sublist) of python-qua-binary, in the verse-qua-binary list —— remember, chunk IS the sublist, not an index
        verselineindex = list2.index(chunk) ###### Here, "verselineindex" IS an index; the index of the verse line that corresponds to the matched binary "chunk"
        chunkoutputlistbylines.append(languagemodelledbylist2[verselineindex])
        ###### actually there should also be a "return chunkoutputlistbylines" here
        ###### actually, does this "if" clause even need to go in the recursive function? Yes, because each chunk needs to be checked as a whole,
        ###### for each recursion
    else:
        splitpoint = int(math.floor(len(chunk)/2))
        findmatch(chunk[:splitpoint], list2, languagemodelledbylist2, chunkoutputlistbylines)
        findmatch(chunk[splitpoint:], list2, languagemodelledbylist2, chunkoutputlistbylines)
        # can you run two recursions simultaneously?
    return chunkoutputlistbylines


    # outputlistbylinesbywords needs to be a universal list because this findmatch function needs to be able to append the verse lines
    # to the outputlist
    # here, in findmatch, you are appending parts of the chunk to one another; at best you do the whole chunk in one go, but the point is that
    # you can, at best, only return the CHUNK. Thus the RESULT of findmatch(chunk, scannedbinarybylinesbywords, scannedinputbylinesbywords)
    # will be the CHUNK in verse, you then need to append that to an outputlist in the other function.
    # In findmatch we will call it CHUNKOUTPUTLISTBYLINES. We will need a separte list, called, e.g., OUTPUTLISTBYLINESBYWORDS in the other function/class
    # So we will need another argument, the CHUNKOUTPUTLISTBYLINES, which will be a list first instatiated in the for loop of the other function/class
    # Calling it "outputlistbylines" not "outputlistbylinesbywords" because we never actually search at the level of words (unless the splits take
    # us there)


    # [[[when], [in], [campus], [boarding]]
    # for run in word
    # [[[when]], [[in]], [[cam], [pus]], [[boar], [ding]]]
    # scannedbinarybylinesbywords = [[[0 for x in y] for y in z] for z in scannedinputbylinesbywords]
    # [[[1]], [[0]], [[1], [0]], [[1], [0]]]
    # [when, in, cam, pus, boar, ding] or [[when], [in], [campus], [boarding]]
    # [1, 0, 1, 0, 1, 0] or [1, 0, 10, 10]
    #
    # so for python input of, say, [1, 0, 1]... no result... and for [1, 0, 1, 0]... still no result.
    # what we want is:

    # ideally you would have: [[1], [0], [1, 0], [1, 0]]

    # two syllable words, two syllable lines of code

    # in which case, for a python input of [[[0]], [[1], [0]]], you search in [[[1]], [[0]], [[1], [0]], [[1], [0]]]
    # and get [[[in]], [[cam], [pus]]]

    # pythoninputbychunksbylines = [x.split('\n') for x in file1.split('\n\n\n')]
    # pythoninputbychunksbylines = [[x for x in y if x != "\n"] for y in pythoninputbychunksbylines]
    # for line in chunk: if line ___some quality of two-syllable python line___, then line = [x for
    # pythoninputbychunksbylines = [[x for x in z] for z in y] for y in pythoninputbychunksbylines]
    #
    #
    # pythonbinarybychunksbylines = [[0 for x in y] for y in pythoninputbychunksbylines]

def highlight(s, regexes):
    """Highlight all instances of regexes in s."""

    # Get intervals for which strings match
    intervals = []
    for regex in regexes:
        if not regex:
            continue
        matches = re.finditer(regex, s, re.MULTILINE)
        for match in matches:
            intervals.append((match.start(), match.end()))
    intervals.sort(key=lambda x: x[0])

    # Combine intervals to get highlighted areas
    highlights = []
    for interval in intervals:
        if not highlights:
            highlights.append(interval)
            continue
        last = highlights[-1]

        # If intervals overlap, then merge them
        if interval[0] <= last[1]:
            new_interval = (last[0], interval[1])
            highlights[-1] = new_interval

        # Else, start a new highlight
        else:
            highlights.append(interval)

    # Maintain list of regions: each is a start index, end index, highlight
    regions = []

    # If no highlights at all, then keep nothing highlighted
    if not highlights:
        regions = [(0, len(s), False)]

    # If first region is not highlighted, designate it as such
    elif highlights[0][0] != 0:
        regions = [(0, highlights[0][0], False)]

    # Loop through all highlights and add regions
    for start, end in highlights:
        if start != 0:
            prev_end = regions[-1][1]
            if start != prev_end:
                regions.append((prev_end, start, False))
        regions.append((start, end, True))

    # Add final unhighlighted region if necessary
    if regions[-1][1] != len(s):
        regions.append((regions[-1][1], len(s), False))

    # Combine regions into final result
    result = ""
    for start, end, highlighted in regions:
        escaped = escape(s[start:end])
        if highlighted:
            result += f"<span>{escaped}</span>"
        else:
            result += escaped
    return result


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
