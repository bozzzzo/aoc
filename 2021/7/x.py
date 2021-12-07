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


def price(a, n):
    return sum(abs(x-n) for x in a)

def first(a):
    a=sorted(a)
    p=sorted((price(a,n), n) for n in range(min(a), max(a)))
    return (p[:5])
    pass

def price2(a, n):
    def d(x,n):
        l=abs(x-n)
        return (l * (l+1)) // 2
    return sum(d(x,n) for x in a)

def irange(a,b):
    d = 1 if b >= a else -1
    return range(a,b+d,d)

def second(a):
    a=sorted(a)
    p=sorted((price2(a,n), n) for n in range(min(a), max(a)))
    return (p[:5])
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
    return tuple(map(int, f.read().strip().split(',')))
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
