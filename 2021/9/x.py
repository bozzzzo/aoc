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


def islow(a, c):
    for dx in (-1,1):
        for dy in (-1,1):
            n = (c[0]+dx, c[1]+dy)
            if n not in a:
                continue
            if a[n] <= a[c]:
                return False
    return True

def findlow(a):
    return filter(lambda c: islow(a,c), a)

def first(a):
    return sum(1+v for c,v in findlow(a))
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
        return tuple(map(int,l.strip()))
    return {(x,y):z for y,row in enumerate(map(parse_line, f)) for x,z in enumerate(row)}
    pass

for name in [("test_input"),
             ("input")][:1
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
