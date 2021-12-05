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


def first(a):
    m = collections.Counter()
    for (x1,y1),(x2,y2) in a:
        if x1 == x2:
            m.update((x1, y)
                     for y in range(min(y1,y2), max(y1,y2)+1))
        elif y1 == y2:
            m.update((x, y1)
                     for x in range(min(x1,x2), max(x1,x2)+1))
    return sum(1 for v in m.values() if v > 1)

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


def _trace(f):
    r = f.readline()
    return r

def parse(f):
    def parse_line(l):
        return tuple(tuple(int(c) for c in t.strip().split(','))
                     for i, t in enumerate(l.split("->")))

    return list(map(parse_line, f))
    pass

for name in [("test_input"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    # print(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)
    #second(a)

print("==================",flush=True)
