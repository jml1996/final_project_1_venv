from __future__ import division, unicode_literals
import codecs
from bs4 import BeautifulSoup
import re
from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
import math
from helpers import lines, sentences, substrings
import random
import operator
import ast
from itertools import chain
import sys
import time
import binascii



def splitfile(file):
    n = 100
    chunks = [file[i:i+n] for i in range(0, len(file), n)]
    return chunks


# a = ["123", "456"]

# # b = [list(x) for x in a]

# c = []

# for x in a:
#     c.append([int(i) for i in x])

# print(a)
# print(c)

print(f"{len([0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0])}")