import functools
import itertools
import re
import collections
import pprint
import operator
import time
from dataclasses import dataclass, replace, field
import numpy as np
from typing import *
from pprint import pprint

def fst(x):
    return x[0]

def snd(x):
    return x[1]

def dbg(*x, **y):
    # print(*x, **y)
    pass

def irange(a,b):
    d = 1 if b >= a else -1
    return range(a,b+d,d)

pairs = dict('() <> [] {}'.split())

class Incomplete(Exception): pass
class Corrupted(Exception):
    def __init__(self, c, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = c

def check(a, i, c):
    o = a[i]
    e = pairs[o]
    i += 1
    while i < len(a):
        if a[i] == e:
            return i+1, c
        elif a[i] in pairs:
            i, c = check(a, i, c)
        else:
            raise Corrupted(a[i])
    else:
        return i, c+e

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def score(l):
    try:
        check(l, 0, '')
    except Corrupted as c:
        return scores[c.c]
    except:
        pass
    return 0

def first(a):
    return sum(map(score, a))
    pass

def complete(l):
    try:
        _, c = check(l, 0, '')
        return c
    except Corrupted:
        return None

def second(a):
    c = tuple(map(complete,a))
    print(c)
    pass

def test():
    def _(a,b):
        assert a==b, f"{a}!={b}"
    _(check('()', 0, ''), (2, ''))
    _(check('(', 0, ''), (2, ')'))
    pass


test()

def strint(x):
    try:
        return int(x)
    except:
        pass
    return x


def parse(f):
    def parse_line(l):
        return l.strip()
    return tuple(map(parse_line, f))
    pass

for name in [("test_input"),
             ("input")][:1
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    #print(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)

print("==================",flush=True)
