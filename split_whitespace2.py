from __future__ import division, unicode_literals
import codecs
import codecs
from bs4 import BeautifulSoup
import urllib

f = codecs.open('Nothing_in_France.html', 'r')
file2 = f.read()
# soup = BeautifulSoup(''.join(html))

# print(soup)
# pretty = soup.prettify()

# html_stripped = " ".join(l.strip() for l in pretty.split("\n"))

# soup = BeautifulSoup(html_stripped)

# print(html_stripped)

scannedinputbylinesbywords = [x.split() for x in file2.split("</p>")]
scannedinputbylinesbywords = [[x for x in y if "\\" not in x] for y in scannedinputbylinesbywords]
scannedinputbylinesbywords = [[x for x in y if "}" not in x] for y in scannedinputbylinesbywords]
print(scannedinputbylinesbywords)
###### USE THIS PRINT: print(scannedinputbylinesbywords) ###### the 'if "\\" not in x' clause should perhaps be replaced by a more advanced
###### strip method that saves elements like, "<b>to\\'92t</b>," that contain both viable words and '\\.'
# Reformats floating "</b>" tags (as in: ['this', '<b>is', '</b>', 'a']) (due to whitespace split).
# And did same for "<b>" tags (even though bolded whitespace seems only to occur in the whitespace between the text and the TRAILING </b> tag).
for line in scannedinputbylinesbywords:
    lineindex = scannedinputbylinesbywords.index(line)
    for word in line:
        wordindex = scannedinputbylinesbywords[lineindex].index(word)
        if word == "</b>":
            # Literally pastes the </b> end-tag onto the end of the preceding word, and deletes the list-element that was previously occupied
            # by the </b> end-tag.
            q = scannedinputbylinesbywords[lineindex][wordindex - 1]
            scannedinputbylinesbywords[lineindex][wordindex - 1] = q + "</b>"
            scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])
        elif word == "<b>":
            q = scannedinputbylinesbywords[lineindex][wordindex + 1]
            scannedinputbylinesbywords[lineindex][wordindex + 1] = "<b>" + q
            scannedinputbylinesbywords[lineindex].remove(scannedinputbylinesbywords[lineindex][wordindex])
print(scannedinputbylinesbywords)
print("\n")

for line in scannedinputbylinesbywords:
    lineindex = scannedinputbylinesbywords.index(line)
    for word in line:
        wordindex = scannedinputbylinesbywords[lineindex].index(word)
        wordaslist = list(word)
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

###### clause for if first element of word is </b> tag, add that tag to the previous word, and replace it with a space (as first element of current word)
print("\n")
print(scannedinputbylinesbywords)
# Creates binary list that is, so to speak, isomorphic to the list of the words of the original (following the floating-tag-reformatting above)
# (Same thing as was done for the pythonbinary___ list-creation from the pythoninput___ original, above.)
scannedbinarybylinesbywords = [[0 for x in y] for y in scannedinputbylinesbywords]

# For-loop uses BeautifulSoup html scraper to identify occurences of the bold <b></b> tag and replace these occurences with 1's,
# while still maintaining a list structure in which each line of verse is a list of words, and where multisyllabic words are sublists.
# E.g.:
# [['<b>This</b>', 'is', 'a', '<b>', 'bold</b>ed', '<b>text.</b>'], ['And', '<b>this', '</b>', 'is', '<b>too.</b></div>']]
# became (from prev for-loop):
# [['<b>This</b>', 'is', 'a', '<b>bold</b>ed', '<b>text.</b>'], ['And', '<b>this</b>', 'is', '<b>too.</b></div>']]
# which, in the below for-loop, becomes:
# [['<b>This</b>', 'is', 'a', [<b>bold</b>, 'ed'], '<b>text.</b>'], ['And', '<b>this</b>', 'is', '<b>too.</b></div>']]
# Meanwhile,
#          [[0, 0, 0, 0, 0], [0, 0, 0, 0]]
# becomes: [[1, 0, 0, [1, 0], 1], [0, 1, 0, 1]]
for line in scannedinputbylinesbywords:
    lineindex = scannedinputbylinesbywords.index(line)
    for word in line:
        wordindex = scannedinputbylinesbywords[lineindex].index(word)
        soup = BeautifulSoup(''.join(word))
        # This "try-except" method came about because I want to strip the word down until it is of the form '<b>This</b>' or 'is,'
        # but the only way I know I have stripped it down (which I do with BeautifulSoup's "unwrap()" function) far enough,
        # is if I get an AttributeError. Perhaps there is a better way of doing this, but this one seems to work.
        try:
            soup.contents
            soup.html.unwrap()
            soup.contents
            soup.body.unwrap()
            soup.contents
        except AttributeError:
            pass
        # I am here making use of the feauture of BeautifulSoup that originally struck me as annoying, namely that it automatically splits
        # "is a <b>bold</>ed" into ['is', 'a', <b>bold</b>, 'ed']. But I can't have that. I need <b>bold</b> and 'ed' in the same sublist.
        # So I just did soup.contents after I had already for-looped my way into the word [<b>bold</b>ed]. soup.contents of [<b>bold</b>ed]
        # is [<b>bold</b>, 'ed']. So I just set that result (syllables) to be the value of the given "word" in scannedinputbylinesbywords.
        # But: all of this ONLY if the word is multi-syllabic!
        syllables = soup.contents
        if len(syllables) > 1:
            # Adjusting the scannedbinary list structure
            scannedbinarybylinesbywords[lineindex][wordindex] = [0 for x in range(len(syllables))]
            # Adjusting the scannedinput list structure (see the above explanation of this "if len(syllables) > 1"-clause)
            scannedinputbylinesbywords[lineindex][wordindex] = soup.contents
            # Finds words with the bold ("<b></b>") tag. (In the case of tri-syllabic words, for example, there could be more than one such tag.)
            q = soup.find_all("b")
            # Okay, so let us suppose a tri-syllabic word like [<b>bold</b>, 'ed', <b>er</b>] which is not a word, but so be it.
            # What we want is [1, 0, 1].
            # q (= soup.find_all("b")) would look like this: [<b>bold</b>, <b>er</b>]
            # We want to say: for 0, then for 1 (i in the range of the length of the q-list), let p be the element at that index in q.
            for i in range(len(q)):
                p = q[i]
                # Now, use p to find the index of that element in SYLLABLES (which, recall, is: [<b>bold</b>, 'ed', <b>er</b>]).
                indexofboldsyllable = syllables.index(p)
                # Now use THAT index, which is the index of the bold syllable in question, let the element at that index in the scannedbinary list
                # be set equal to 1.
                scannedbinarybylinesbywords[lineindex][wordindex][indexofboldsyllable] = 1
        # Otherwise, it's a single-syllabic word and you can just check for the <b> and </b> tags, with the option of trailing whitespace for
        # the latter.
        elif "<b>" and ("</b>" or " </b>") in word:
            scannedbinarybylinesbywords[lineindex][wordindex] = 1