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

b = [[[1, 0], 0, 1, 0], [1, 0, [1, 0, 1], 1]]
a = [[1, 0, 1], 1]

# a = [0, 0, 1]
# b = [1, 0, 1, 0, 1, 0, 0, 1]

print(search(b, a))