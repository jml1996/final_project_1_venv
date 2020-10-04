import operator
import ast

# from: https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
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


pythonbinarybychunksbylinesbykeywords = [[1, 0, [1, 0]], [0, 1, [1, 0], 0, 0, 4, 2]]
scannedbinarybylinesbywords = [[1, 0, 1, 0], [1, 0, [1, 0]], [0, 1, [1, 0], 0], [[1, 0], 0, 0, 4, 2], [0, 1, [1, 0], 0, 0, 4]]

outputlistbylines = []
for pythonchunk in pythonbinarybychunksbylinesbykeywords:
    if pythonchunk in scannedbinarybylinesbywords:
        verselineindex = scannedbinarybylinesbywords.index(pythonchunk)
        pythonchunkasverseline = scannedinputbylinesbywords[verselineindex]
        outputlistbylines.append(pythonchunkasverseline)
    else:
        # print(pythonchunk, f"chunk to be searched")
        pythonchunkindex = pythonbinarybychunksbylinesbykeywords.index(pythonchunk)


        chunkelementsindicesofincidence = []
        for pythonline in pythonchunk:
            indicesofincidence = []
            chunkelementsindicesofincidence.append(indicesofincidence)
            # print(pythonline, f"line to be searched")

            for verseline in scannedbinarybylinesbywords:
                # print(verseline, f"verseline")
                if pythonline in verseline:



                    listofduplicates = list_duplicates_of(verseline, pythonline)
                    if len(listofduplicates) == 1:
                        indicesofincidence.append(verseline.index(pythonline))
                    else:
                        print(listofduplicates)
                        indicesofincidence.append(listofduplicates)
                        # for i in range(len(listofduplicates) - 1):
                        #     indexofnextinstance = listofduplicates.pop(0)
                        #     indicesofincidence.append(indexofnextinstance)






                else:
                    indicesofincidence.append(0)
        print(chunkelementsindicesofincidence)
        checksperelement = len(scannedbinarybylinesbywords)
        rating = 0
        scannedbinarylinesrated = {}
        for verseline in scannedbinarybylinesbywords:
            verselineasstring = str(verseline)
            scannedbinarylinesrated[verselineasstring] = 0 ###### A problem: https://stackoverflow.com/questions/10664856/make-dictionary-with-duplicate-keys-in-python
        for i in range(len(chunkelementsindicesofincidence) - 1, 0, -1): # start from end, iterate down
            for j in range(checksperelement - 1, -1, -1): ###### why not end at 0?
                elementjthlist = chunkelementsindicesofincidence[i][j]
                prevelementjthlist = chunkelementsindicesofincidence[i-1][j]
                print(elementjthlist, f"!")
                print(prevelementjthlist, f"?")
                if type(elementjthlist) is list and type(prevelementjthlist) is list:
                    for subincidence in elementjthlist:
                        for prevsubincidence in prevelementjthlist:
                            if subincidence - prevsubincidence == 1:
                                chunkelementsindicesofincidence[i][j] = subincidence
                                chunkelementsindicesofincidence[i-1][j] = prevsubincidence
                                break
                    else:
                        chunkelementsindicesofincidence[i][j] = subincidence
                        chunkelementsindicesofincidence[i-1][j] = prevsubincidence
                elif type(elementjthlist) is list:
                    for subincidence in elementjthlist:
                        if subincidence - prevelementjthlist == 1:
                            chunkelementsindicesofincidence[i][j] = subincidence
                            break
                    else:
                        chunkelementsindicesofincidence[i][j] = subincidence
                elif type(prevelementjthlist) is list:
                    for prevsubincidence in prevelementjthlist:
                        if elementjthlist - prevsubincidence == 1:
                            chunkelementsindicesofincidence[i-1][j] = prevsubincidence
                            break
                    else:
                        chunkelementsindicesofincidence[i-1][j] = prevsubincidence

                if (chunkelementsindicesofincidence[i][j] - chunkelementsindicesofincidence[i-1][j]) == 1:
                    # rated by consecutive matches
                    # scannedbinarylinesrated[rating + 1] = dictionary[rating]
                    # del dictionary[rating]
                    #scannedbinarylinesrated.update({rating: scannedbinarybylinesbywords[j] for scannedbinarybylinesbywords[j] in scannedbinarybylinesbywords})
                    verselineas = str(scannedbinarybylinesbywords[j])
                    scannedbinarylinesrated[verselineas] += 1
                    # update({scannedbinarybylinesbywords[j]: i += 1})
                    print(scannedbinarylinesrated)


        verseline_binary_as_key_string_to_be_searched = max(scannedbinarylinesrated.items(), key=operator.itemgetter(1))[0] ######
        verseline_binary_as_list_to_be_searched = ast.literal_eval(verseline_binary_as_key_string_to_be_searched)

        verselineindex = scannedbinarybylinesbywords.index(verseline_binary_as_list_to_be_searched)

        #pythonchunkasverseline = scannedinputbylinesbywords[verselineindex]

        for pythonline in pythonbinarybychunksbylinesbykeywords[pythonchunkindex]:

            if pythonline in scannedbinarybylinesbywords[verselineindex]:
                pythonbinary_line_index_in_versebinary_line = scannedbinarybylinesbywords.index(pythonline)
                # pop it so that there are no duplicates; we don't need this value in....
                # nope; can't pop it; that would change indices...
                pythonlineasverseword = scannedinputbylinesbywords[verselineindex][pythonbinary_line_index_in_versebinary_line]
                if (scannedbinarybylinesbywords[verselineindex].count(1) > 1) and (scannedbinarybylinesbywords[verselineindex].count(0) > 1):
                    scannedinputbylinesbywords[verselineindex][pythonbinary_line_index_in_versebinary_line] = None
                outputlistbylines.append(pythonlineasverseword)









                #scannedinputbylinesbywords[verselineindex][pythonbinary_line_index_in_versebinary_line] = None
                # nope; can't set it to None; what if there are no more 1's or 0's left?
                #fixed








#if pythonline


#     outputlistbylines.append(pythonchunkasverseline)
# ast.literal_eval(max(b.items(), key=operator.itemgetter(1))[0])

                    # mins = [] #len(elementjthlist) - 1 + len prevelementjthlist - 1
                    # for subincidence in elementjthlist:
                    #     mins.append(min(prevelementjthlist, key=lambda x:abs(x - subincidence - 1))
                    # for revmin in mins:
                    #     minother = min(elementjthlist, key=lambda x:abs((x - minprev) - 1))
# >>> stats = {'a':1000, 'b':3000, 'c': 100, 'd':3000}
# >>> max(stats.iteritems(), key=operator.itemgetter(1))[0]

                    ############## AHHHHHHHHHHHHHHHHHHHHH