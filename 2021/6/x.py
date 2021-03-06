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


def day(a):
    def fish(a):
        new = []
        for c in a:
            if c == 0:
                yield 6
                new.append(8)
            else:
                yield c - 1
        yield from new
    return tuple(fish(a))

def cday(c):
    r = collections.Counter()
    for day, count in c.items():
        if day == 0:
            r[6] += count
            r[8] += count
        else:
            r[day-1] += count
    return r

def first(a):
    for d in range(1,19):
        a = day(a)
        print(f"After {d} day:", a)
    for d in range(19,81):
        a = day(a)
    print(len(a))

def irange(a,b):
    d = 1 if b >= a else -1
    return range(a,b+d,d)

def second(a):
    c = collections.Counter(a)
    print("initial", a, c)
    def total(c):
        return sum(c.values())
    for d in range(1, 81):
        c = cday(c)
        if d < 5:
            print(d, c)
    print("after 80", total(c))
    for d in range(81, 257):
        c = cday(c)
    print("after 256", total(c))
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
    return tuple(map(int, f.read().strip().split(',')))
    pass

for name in [("test_input"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    #print(a)

    #w = first(a)
    #print("first", w)
    w = second(a)
    print("second", w)
    #second(a)

print("==================",flush=True)
