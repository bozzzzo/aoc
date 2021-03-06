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


def neigbor(a, c):
    for dx, dy in ((-1,0), (1, 0), (0, -1), (0, 1)):
        n = (c[0]+dx, c[1]+dy)
        if n not in a:
            continue
        yield n

def islow(a, c):
    #print()
    for n in neigbor(a,c):
        #print(c,a[c],n,a[n])
        if a[n] <= a[c]:
            return False
    return True

def findlow(a):
    return {c:v for c,v in a.items() if islow(a, c)}

def first(a):
    low = findlow(a)
    # print(low)
    return sum(1+v for c,v in low.items())
    pass

def basin(a, l):
    b = set()
    p = set((l,))
    while p:
        c = p.pop()
        b.add(c)
        for n in neigbor(a,c):
            if a[n] == 9 or n in b or n in p:
                continue
            p.add(n)
    return len(b)

def second(a):
    low = findlow(a)
    basins = sorted(basin(a,l) for l in low)
    #print(basins)
    return functools.reduce(operator.mul, basins[-3:])
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

print("==================",flush=True)
