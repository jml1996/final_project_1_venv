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

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
def encode_string_binary(s):
    return ''.join([bin(ord(c))[2:].rjust(8,'0') for c in s])

print(f"{encode_string_binary('abcd')}")

print(f"{list(encode_string_binary('abcd'))}")