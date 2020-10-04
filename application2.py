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

    # chunks == lines; lines == words; keyword-clauses == syllables (in multisyllabic words)

    pythoninputbychunksbylinesbykeywords = []

    pythoninputbychunksbylinesbykeywords = [x.split('\n') for x in file1.split('\n\n\n')] # this is still just lines

    pythoninputbychunksbylinesbykeywords = [[x for x in y if x != ""] for y in pythoninputbychunksbylinesbykeywords] # no need for "\n" just "" (see visualizer)

    pythonbinarybychunksbylinesbykeywords = [[0 for x in y] for y in pythoninputbychunksbylinesbykeywords]

    for chunk in pythoninputbychunksbylinesbykeywords:
        chunkindex = pythoninputbychunksbylinesbykeywords.index(chunk)
        for line in chunk:
            lineindex = pythoninputbychunksbylinesbykeywords[chunkindex].index(line)
            if (len(set(line).intersection(______keywords______))) == 1:
                pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1]
            elif (len(set(line).intersection(______keywords______))) == 2:
                pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1, 0, 1] # line was previously: 0; now it is: [0, 1, 0, 1]
            elif "=" in line:
                pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = 1 # line was previously 0 (but it was IN []);
                # two chunks: [[], []]
                # two lines in each chunk: [["line=1", "line=2"], ["line1*", "line2*"]]; [[0, 0], [0, 0]]
                # for chunk index 1, line index 2: "line=2"
                # if chunk index 1, line index 2 includes an equals sign in input, make it 1 in output: 1
                # output (binary): [[0, 1], [0, 0]]
                #
                # else if it has two keywords, let the 0 (line2*, say) equal [0, 1]: [[0, 1], [0, [0, 1]]]

                # Now, the recursion will work for a given CHUNK: [0, [0, 1]]
                # check the word. A word can be like this: 1; or like this: [0, 1]


    # equals statements should take the form: "1, 0, 1"
    # "if x: q = p" should be: "[0, 1, 0], [1, 0, 1]"

    # equals: 1
    # if x: 0, 1
    # if x in y: 0, 1, 0, 1


    pythoninputbychunksbylines = []

    # nested list, split first around the chunks (two blank lines) (which will be equivalent to lines of verse), then around lines (words of verse)
    pythoninputbychunksbylines = [x.split('\n') for x in file1.split('\n\n\n')]

    # going from [['a'], ['xyz', '\n', 'pdq']] to [['a'], ['xyz', 'pdq']]?
    pythoninputbychunksbylines = [[x for x in y if x != "\n"] for y in pythoninputbychunksbylines]

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

    for line in scannedinputbylinesbywords:
        lineindex = scannedinputbylinesbywords.index(line) # ADDED: identifies location of line within entire input verse list
        for word in line:
            wordindex = scannedinputbylinesbywords[lineindex].index(word) # ADDED: identifies location of word within line list
            if word.bold:
                scannedbinarybylinesbywords[lineindex][wordindex] = 1 ###### THESE ARE NOT INDICES; you need to find exact index of the line and word

    # Getting bolded text: https://stackoverflow.com/questions/27904470/checking-for-particular-style-using-python-docx
    # uses "from docx import *"


    outputlistbylinesbywords = []

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

# As of 11/30/17 at 8:17 PM: def findmatch(chunk, scannedbinarybylinesbywords == list2, scannedinputbylinesbywords == languagemodelledbylist2, chunkoutputlistbylines)

def findmatch(chunk, list2,  languagemodelledbylist2, chunkoutputlistbylines):
    if chunk in list2: # IF there is an IDENTICAL match for the whole chunk (a sublist) of python-qua-binary, in the verse-qua-binary list —— remember, chunk IS the sublist, not an index
        verselineindex = list2.index(chunk) ###### Here, "verselineindex" IS an index; the index of the verse line that corresponds to the matched binary "chunk"
        chunkoutputlistbylines.append(languagemodelledbylist2[verselineindex])

    else:
        splitpoint = int(math.floor(len(chunk)/2))
        findmatch(chunk[:splitpoint], list2, languagemodelledbylist2, chunkoutputlistbylines)
        findmatch(chunk[splitpoint:], list2, languagemodelledbylist2, chunkoutputlistbylines)
        # can you run two recursions simultaneously?
    return chunkoutputlistbylines



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


    # contra the "ideally" statement above:
    # Why not just [1, 0, [1, 0], [1, 0]]? and then you leave 1 and 0 in python  when they are singltons...
    # this: pythonbinarybychunksbylines[chunkindex][lineindex] = 1
    # and this: pythonbinarybychunksbylines = [[0 for x in y] for y in pythoninputbychunksbylines]
    # could remain



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
