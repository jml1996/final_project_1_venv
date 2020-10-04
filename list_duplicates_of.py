# from: https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

source = [1, 0, [1, 0]]
print(list_duplicates_of(source, [1, 0]))