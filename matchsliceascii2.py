import random
import codecs
from bs4 import BeautifulSoup
import re
from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
import math
import random
import operator
import ast
from itertools import chain
import sys
import time
import binascii


# inputlist: ascii as binary in list form
# databasebinary: binary representation of verse
# databaseverse: verse (html, isomorphic to databasebinary)
# outputlist: not isomorphic to anything; the structure is meaningless, except that instances of
#  nested lists should be limited to multisyllabic words.
# inputlist: ascii as binary in list form
# databasebinary: binary representation of verse
# databaseverse: verse (html, isomorphic to databasebinary)
# outputlist: not isomorphic to anything; the structure is meaningless, except that instances of
#  nested lists should be limited to multisyllabic words.
def randomslicematch(inputlist, databasebinary, databaseverse, outputlist, recursiondepth):
    for y in range(0, len(inputlist)):
        if recursiondepth > 2:
            # abort(400, f"Recursion depth error. Recursion depth: {recursiondepth}")
            return "YAHOO"
        rand = 0
        if len(inputlist) == 0:
            return outputlist
        # Used to be:
        # if len(inputlist) > 4:
        #   rand = random.randrange(1, 5)
        if len(inputlist) > 3:
            rand = random.randrange(1, 4)
        elif len(inputlist) <= 4:
          rand = random.randrange(1, (len(inputlist) + 1))
        timeout = time.time() + .0001
        randomdatabaseindex = random.randrange(0, len(databasebinary))
        randomindexinindex = random.randrange(0, len(databasebinary[randomdatabaseindex]))
        if len(inputlist) == 1:
            slicetobefound = inputlist[0]
            while slicetobefound != databasebinary[randomdatabaseindex][randomindexinindex]:
                randomdatabaseindex = random.randrange(0, len(databasebinary))
                randomindexinindex = random.randrange(0, len(databasebinary[randomdatabaseindex]))
                if time.time() > timeout:
                    abort(400, f"no word found for ascii-as-binary slice: {slicetobefound}")
            slicetobefoundasverseword = databaseverse[randomdatabaseindex][randomindexinindex]
            outputlist.append(slicetobefoundasverseword)
            return outputlist
        slicetobefound = inputlist[0:rand]
        if len(slicetobefound) == 1:
            slicetobefound = slicetobefound[0]
        while slicetobefound != databasebinary[randomdatabaseindex][randomindexinindex]:
            randomdatabaseindex = random.randrange(0, len(databasebinary))
            randomindexinindex = random.randrange(0, len(databasebinary[randomdatabaseindex]))
            if time.time() > timeout:
                return randomslicematch(inputlist, databasebinary, databaseverse, outputlist, (recursiondepth + 1))
                #abort(400, f"no word found for ascii-as-binary slice2: {slicetobefound}")
        slicetobefoundasverseword = databaseverse[randomdatabaseindex][randomindexinindex]
        outputlist.append(slicetobefoundasverseword)
        inputlist = inputlist[rand:len(inputlist)]
        print(f"inputlist: {inputlist}")
        print(f"outputlist: {outputlist}")
        print(f"recursiondepth: {recursiondepth}")



    
#return only outputlist? rather than breaking it?


x = [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
baseasbinary = [[[1, 0], [1, 0, 1]], [0, [1, 0], 1], [0, [1, 0], 0], [[1, 0], [0, 1], 0], [1, [0, 1, 0], [1, 0]], [[1, 0, 0], 0], [1, [0, 1, 0, 1]]]
baseasverse = [[['hell', 'o'], 'Josh', 'I', 'have'], ['a', ['quest', 'tion'], 'you'], ['might', ['an', 'swer'], 'the'], [['peo', 'ple'], ['ma', 'lign'], 'me'], ['so', ['ar', 'raign', 'ments'], ['foll', 'ow']], [['a', 'ny', 'way'], 'we'], ['are', ['ap', 'plic', 'a', 'ble']]]
z = []
recursiondepth = 0

# randomslicematch(x, baseasbinary, baseasverse, z)

print(f"Result: {randomslicematch(x, baseasbinary, baseasverse, z, recursiondepth)}")
