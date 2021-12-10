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

def check(a, i):
    o = a[i]
    e = pairs[o]
    i += 1
    while i < len(a):
        if a[i] == e:
            return i+1
        elif a[i] in pairs:
            i = check(a, i)
        else:
            raise Corrupted(a[i])
    else:
        raise Incomplete()

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def score(l):
    try:
        check(l, 0)
    except Corrupted as c:
        return scores[c.c]
    except:
        pass
    return 0

def first(a):
    return sum(map(score, a))
    pass

def second(a):
    pass

def test():
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
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    print(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)

print("==================",flush=True)
