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

a = [[1, 0, [1, 0, 1], 1], [0, [1, 0, 1], 0, 1, 0], [9, 7, [10, 11], 1, 2]]
b = [0, 0]

# a = [['this', 'this'], ['if', 'if'], 'this', 'if', 'this']
# b = [0, 0]


print(type(flatten(a)))
print(flatten(a))

print(type(flatten(b)))
print(flatten(b))