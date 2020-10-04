from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    alines = []
    blines = []

    alines = a.split("\n")
    blines = b.split("\n")

    overlap = list(set(alines).intersection(blines))
    overlap1 = [x for x in overlap if x != ""]

    return overlap1

    # For "set().intersection()": https://stackoverflow.com/questions/642763/find-intersection-of-two-lists
    # For recasting the set as a list: https://stackoverflow.com/questions/6828722/python-set-to-list
    # For "[x for x in overlap if x != ""]" as a way to get rid of a blankline: https://stackoverflow.com/questions/7347063/remove-a-n-list-item-from-a-python-list
    # For reassuring me that I was seriously overcomplicating things by trying to include a for loop and the append function
    # to accomplish what "a.split" and "b.split" were already doing: Ethan Sciamma.

    # ((Not sure why there are so many "\" when I submit code as textfiles. But cs50 shows all green, so I'll just assume this has to do
    # some of the provided code.))


def sentences(a, b):
    """Return sentences in both a and b"""
    asentences = []
    bsentences = []
    asentences = sent_tokenize(a)
    bsentences = sent_tokenize(b)
    return list(set(asentences).intersection(bsentences))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    asubstrings = []
    bsubstrings = []

    for i in range(0, (len(a) - n + 1)):
        asubstrings = asubstrings + [a[i:i + n]]
        # This a[i:i+n] formulation courtesy of Ethan Sciamma. Before talking with him, I had thought of the for loop as being tasked
        # with finding ALL the substrings of a GIVEN substring (of size n), but in fact it (or rather, each iteration of it; each i) need only
        # find ONE such substring of the WHOLE of string a, as long as that substring is of size n.
        # That is: it is precisely via the iteration of i that we are picking our substrings.
        # Or, more clearly: I had been thinking of n as the string of which we wanted to find the substrings, when in fact (obvious, now)
        # it is the pre-ordained size of ALL substrings, so we need only march it along the range of the a or b string, by means of i.

    for i in range(0, (len(b) - n + 1)):
        bsubstrings = bsubstrings + [b[i:i + n]]

    overlap = list(set(asubstrings).intersection(bsubstrings))
    overlap1 = [x for x in overlap if x != "\n"]

    return overlap1
