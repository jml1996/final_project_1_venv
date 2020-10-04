from __future__ import division, unicode_literals
import codecs
import codecs
from bs4 import BeautifulSoup

f = codecs.open("Bold_text.html", 'r')
file2 = f.read()



# scannedinputbylinesbywords was previously "bywhitespace"

scannedinputbylinesbywords = [x.split() for x in file2.split("<div>")]
print(scannedinputbylinesbywords)

for line in scannedinputbylinesbywords:
    lineindex = scannedinputbylinesbywords.index(line)
    for word in line:
        wordindex = scannedinputbylinesbywords[lineindex].index(word)
        if word == "</b>":
            q = scannedinputbylinesbywords[lineindex][wordindex - 1]
            scannedinputbylinesbywords[lineindex][wordindex - 1] = q + "</b>"
            scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])
            #scannedbinarybylinesbywords[lineindex].remove(scannedbinarybylinesbywords[lineindex][wordindex])
            ##scannedinputbylinesbywords = [scannedinputbylinesbywords[lineindex][wordindex - 1] + scannedinputbylinesbywords[lineindex][wordindex] for scannedinputbylinesbywords[lineindex][wordindex - 1] in scannedinputbylinesbywords]
        elif word == "<b>":
            q = scannedinputbylinesbywords[lineindex][wordindex + 1]
            scannedinputbylinesbywords[lineindex][wordindex + 1] = "<b>" + q
            scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])
            #scannedbinarybylinesbywords[lineindex].remove(scannedbinarybylinesbywords[lineindex][wordindex])

print(scannedinputbylinesbywords)

scannedbinarybylinesbywords = [[0 for x in y] for y in scannedinputbylinesbywords]
print(scannedbinarybylinesbywords)

#print(scannedinputbylinesbywords)

for line in scannedinputbylinesbywords:
    lineindex = scannedinputbylinesbywords.index(line)
    for word in line:
        wordindex = scannedinputbylinesbywords[lineindex].index(word)
        soup = BeautifulSoup(''.join(word))
        # soup.p.unwrap()
        try:
            soup.contents
            soup.html.unwrap()
            soup.contents
            soup.body.unwrap()
            soup.contents
        except AttributeError:
            pass
        syllables = soup.contents
        print(syllables)
        if len(syllables) > 1:
            scannedbinarybylinesbywords[lineindex][wordindex] = [0 for x in range(len(syllables))]
            scannedinputbylinesbywords[lineindex][wordindex] = soup.contents
            q = soup.find_all("b")
            indexofboldsyllable = 0
            for i in range(len(q)):
                p = q[i]
                indexofboldsyllable = syllables.index(p)
                scannedbinarybylinesbywords[lineindex][wordindex][indexofboldsyllable] = 1
        elif "<b>" and ("</b>" or " </b>") in word:
            scannedbinarybylinesbywords[lineindex][wordindex] = 1



            # soup.find("table").find("tbody").find_all("tr")
            # print rows[1].find_all("td")[2].get_text()

            # new_string = 1
            # syllables.findall("b").replace_with(new_string)





print(scannedinputbylinesbywords)
print(scannedbinarybylinesbywords)
