from __future__ import division, unicode_literals
import codecs
from bs4 import BeautifulSoup



html = codecs.open('Bold_text_simple.html', 'r') # "test.html", 'r', 'utf-8')
soup = BeautifulSoup(''.join(html))

print(soup.prettify())

print(soup.contents)

print(soup.body.contents)

# #print(soup.p.contents[1][1])

# soup.html.unwrap()
# print(soup.contents)
# print(str(soup.contents))

# soup.body.unwrap()
# print(soup.contents)

# soup.p.unwrap()
# print(soup.contents)

# # soup1 = BeautifulSoup(markup)

# # print(soup.contents)

# # lala = str((soup.contents))

# # print(lala)

# # a = ''.join(soup.contents)
# # print(a)

# #new_tag = soup.new_tag("")

new_string = "|"+soup.b.text+"|"
soup.findall("b").replace_with(new_string)


# # print(soup.contents)

# # q = soup.p.contents

# # print(q)

# # print(q.b.unwrap)

# # for run in soup.contents:
# #  runindex = soup.contents.index(run)
# #  try:
# #   if soup.contents[runindex][0] != " ":
# #    #''.join(soup.contents[runindex - 1:runindex])
# #    soup.contents[runindex-1] = list(map(list, (zip(soup.contents[runindex - 1], soup.contents[runindex]))))
# #    #soup.contents[runindex-1] = [a+str(b) for a, b in zip(soup.contents[runindex - 1], soup.contents[runindex])]
# #    #soup.p.contents[runindex - 1] = list()
# #  except KeyError:
# #   continue

# # print(soup.contents)

#  # print(soup.p.contents[runindex][0])



#  # for char[0] in run:
#  #  print(char[0])
#  #if not  soup.p.contents[runindex]
