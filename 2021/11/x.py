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

def inc(a, which):
    flashes = []
    b = a.copy()
    for c in which:
        b[c] += 1
        if b[c] == 10:
            flashes.append(c)
    return b, flashes

def neighbors(a, f):
    for x,y in f:
        for dx,dy in [(-1,-1),(0,-1),(1,-1),
                      (-1, 0),       (1, 0),
                      (-1, 1),(0, 1),(1, 1)]:
            c = (x+dx, y+dy)
            if c in a:
                yield c

def zero(a):
    return {c:0 if z > 9 else z for c,z in a.items()}

def step(a):
    b, flashes = inc(a, a)
    all = flashes[:]
    while flashes:
        b, flashes = inc(b, neighbors(a, flashes))
        all.extend(flashes)
    b = zero(b)

    return b, all


def show(a):
    mx, my = max(a)
    print("\n".join("".join(str(a[(x,y)]) for y in range(my+1)) for x in range(mx+1)))

def first(a):
    b, f = step(a)
    show(b)
    print(len(f), f)
    b, f = step(b)
    show(b)
    print(len(f), f)
    b, f = step(b)
    show(b)
    print(len(f), f)
    pass




def second(a):
    pass

def test():
    def _(a,b):
        print()
        assert a==b, f"{a}!={b}"
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
    return {(x,y):int(z)  for x, l in enumerate(f) for y,z in enumerate(parse_line(l))}
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
