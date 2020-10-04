scannedinputbylinesbywords = [['<b>Rain ', '</b>to'], ['<b>the', '</b>none-<b>sparing', '<b>war</b>?']]
for line in scannedinputbylinesbywords:
    lineindex = scannedinputbylinesbywords.index(line)
    for word in line:
        wordindex = scannedinputbylinesbywords[lineindex].index(word)
        wordaslist = list(word)
        print(wordaslist[:4])
        if wordaslist[:4] == ['<', '/', 'b', '>']:
            prevwordaslist = list(scannedinputbylinesbywords[lineindex][wordindex-1])
            del wordaslist[:3]
            wordaslist[0] = ' '
            if prevwordaslist[(len(prevwordaslist))-1] == ' ':
                del prevwordaslist[(len(prevwordaslist))-1]
            prevwordaslist.append("</b>")
            wordlistasstring = ''.join(wordaslist)
            prevwordlistasstring = ''.join(prevwordaslist)
            scannedinputbylinesbywords[lineindex][wordindex] = wordlistasstring
            scannedinputbylinesbywords[lineindex][wordindex-1] = prevwordlistasstring

print(scannedinputbylinesbywords)

elif wordaslist[:3] == ['<', 'b', '>'] and (wordaslist[(len(wordaslist)-1) - 4:] == ['<', '/', 'b', '>', '?'] or wordaslist[(len(wordaslist)-1) - 3:] == ['<', '/', 'b', '>']):
                wordlistasstring = ''.join(wordaslist)
                scannedinputbylinesbywords[lineindex][wordindex] = 1