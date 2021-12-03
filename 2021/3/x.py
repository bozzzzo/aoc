import functools
import itertools
import re
import collections
import pprint
import operator
import time
from dataclasses import dataclass
import numpy as np
from pprint import pprint

def fst(x):
    return x[0]

def snd(x):
    return x[1]

def dbg(*x, **y):
    # print(*x, **y)
    pass


def first(a):
    bits = tuple(map(sum, map(lambda x: map(int,x), zip(*a))))
    print(tuple(bits), ['1' if b > b/len(bits) else '0' if b < b/len(bits) else '=' for b in bits])


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

def parse(x):
    return x

for name in [("test_input"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = tuple(parse(l.strip()) for l in f)
    #print(a)

    first(a)

print("==================",flush=True)
