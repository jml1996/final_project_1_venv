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
    return flatl


def deflatten(flattenedindex, originallist):
    digitcount = -1
    originalliststartindex = ""
    while digitcount <= flattenedindex:
        for item in originallist:
            itemindex = originallist.index(item)
            if type(item) is list:
                for item2 in item:
                    item2index = item.index(item2)
                    if type(item2) is list:
                        for item3 in item2:
                            item3index = item2.index(item3)
                            digitcount += 1
                            if digitcount == flattenedindex:
                                # https://stackoverflow.com/questions/13341853/convert-string-to-nested-list-with-python
                                originalliststartindex = f"{itemindex}-{item2index}-{item3index}"
                                break
                    else:
                        digitcount += 1
                        if digitcount == flattenedindex:
                                # https://stackoverflow.com/questions/13341853/convert-string-to-nested-list-with-python
                                originalliststartindex = f"{itemindex}-{item2index}"
                                break
            else:
                digitcount += 1
                if digitcount == flattenedindex:
                                # https://stackoverflow.com/questions/13341853/convert-string-to-nested-list-with-python
                                originalliststartindex = f"{itemindex}"
                                break
    return originalliststartindex

orig = [[1, 0, [1, 0, 1], 1], [0, [1, 0, 1], 0, 1, 0], [9, 7, [10, 11], 1, 2]]
b = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 9, 7, 10, 11, 1, 2]

# print(type(flatten(a)))
# print(flatten(a))
# q = 15

print(b[15])
q = deflatten(15, orig).split('-')
a = []
for segment in q:
    a.append(int(segment))
try:
    x = a[0]
    y = a[1]
    z = a[2]
except IndexError:
    pass
    try:
        x = a[0]
        y = a[1]
    except IndexError:
        pass
        try:
            x = a[0]
        except IndexError:
            pass

print(orig[x][y][z])

# >>> path = '1-3-6-3-6'
# >>> element = a
# >>> for segment in path.split('-'):
#         element = element[int(segment)]