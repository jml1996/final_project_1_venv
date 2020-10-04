import codecs
import re

f = codecs.open("python_text.rtf", 'r')
file1 = f.read()

pythoninputbychunksbylinesbykeywords = []

pythoninputbychunksbylinesbykeywords = [x.split('\n') for x in file1.split('\n\n\n')] # this is still just lines

#print(pythoninputbychunksbylinesbykeywords)

pythoninputbychunksbylinesbykeywords = [[x for x in y if x != ""] for y in pythoninputbychunksbylinesbykeywords] # no need for "\n" just "" (see visualizer)

#print(pythoninputbychunksbylinesbykeywords)

pythonbinarybychunksbylinesbykeywords = [[0 for x in y] for y in pythoninputbychunksbylinesbykeywords]

#print(pythonbinarybychunksbylinesbykeywords)

# Python keywords
# Removed:
# 'elif ' because of "if"
# 'for ' because of "or"
# 'not ' because always compounded with another
# Changes:
# ' ' added to end of all but "print", "yield", "None", "True", and "False"
# 'else:' used instead of 'else '
keywords = [
    'and ', 'assert ', 'break ', 'class ', 'continue ', 'def ',
    'del ', 'else:', 'except ', 'exec ', 'finally ',
    'from ', 'global ', 'if ', 'import ', 'in ',
    'is ', 'lambda ', 'or ', 'pass ', 'print',
    'raise ', 'return ', 'try ', 'while ' , 'yield',
    'None', 'True', 'False',
    ]

for chunk in pythoninputbychunksbylinesbykeywords:
    chunkindex = pythoninputbychunksbylinesbykeywords.index(chunk)
    for line in chunk:
        lineindex = pythoninputbychunksbylinesbykeywords[chunkindex].index(line)
        q = []
        for x in keywords:
            if re.findall(x, line) != []:
                q.append(x)
        print(q)
        if (len(q)) == 1:
            pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1]
        elif (len(q)) == 2:
            pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = [0, 1, 0, 1] # line was previously: 0; now it is: [0, 1, 0, 1]
        elif "=" in line:
            pythonbinarybychunksbylinesbykeywords[chunkindex][lineindex] = 1

print(pythoninputbychunksbylinesbykeywords)
print(pythonbinarybychunksbylinesbykeywords)