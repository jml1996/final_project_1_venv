# final_project_1_venv
CS50 final project from December 2017.

Updated a bit in October 2020.

It essentially converts ascii text to binary, then encodes that binary into English according to the marking system of formal poetic <a href=https://en.wikipedia.org/wiki/Scansion>scansion</a>. 

It's built to handle an html rendition of <a href=http://www.shakespearescanned.com/> this </a> database of Shakespeare, scanned by a dude named Richard Leed. 

Leed bolds accented syllables, and, if the user converts this rtf text to html (such that bolded syllables are labelled with <b</b> tags, as outputted by <a href=https://www.textfixer.com/html/convert-word-to-html.php>this</a> word to html converter (see the index.html page for further instructions on this)

— if the user converts this rtf text to html, it can then be converted to a tree consisting of binary representations of the words, with accented (bolded) syllables being represented by 1s, unaccented syllables being represented by 0s.

Multi-syllabic words are represented by lists, nested one layer deeper than single-syllable words.

So, for example, this sentence:

“<b>Words</b> of a <b>sin</b>gle <b>syl</b>lable”

Would be represented first like this:

scannedwordstree = [“<b>Words</b>”, “of”, “a”, [“<b>sin</b>“, “gle”], [“<b>syl</b>“, “la”, “ble”]]

Then like this:

binarytree = [1, 0, 0, [1, 0], [1, 0, 0]]

Then random sections of the ascii binary representation of the input text file* will search (also randomly) for matching sections of binarytree, and from those sections it will move to scannedwordstree and for the output.

The simplest way to get it running is to cd into the directory, (1) get the virtual environment going (in terminal: python3 -m venv venv followed by . venv/bin/activate); and (2) start flask (in terminal: export FLASK_APP=application.py followed by flask run).

Then you can navigate to the local host and upload the file (included in the final_project_1_venv directory (the zip attached here)) titled "python_text.txt" into the python text upload spot — then upload "alls_well_test.txt" (also in the attached directory) into the scanned verse upload spot.

Then it will output the original python ascii text file on the left and its binary representation as scanned verse on the right.

In your terminal, the program will also print a very large list representing the ascii binary for all the characters in the python text file.

The point here is that, because the English language is accented in a fairly rigid manner (as native speakers, we would almost never read the word "fairly" as fairLEE or "english" as "engLISH"), one could theoretically remove the bold tags from the output and still convert the (immense) english-language output back to binary and from there back to the ascii characters.


*In the original project, the functionality was dependent upon the input text being python code specifically, because I was using python keywords to go from python to binary, rather than using the more unambiguous ascii to binary representation method; however, in the current version, the input text could in theory be any ascii text.
