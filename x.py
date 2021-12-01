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
        print(sum(1 for p,n in zip(a[:-1],a[1:]) if n > p))


def second(a):
    def window(s):
        w = []
        for i in s:
            w.append(i)
            if len(w) < 3:
                continue
            elif len(w) == 3:
                w = w[1:]
            yield(sum(w))
    b = list(window(a))
    print(b)
    first(b)
    pass

def test():
    pass


test()

for name in [("test_input"),
             ("input")][:1
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = tuple(int(l.strip()) for l in f)
    print(a)

    second(a)

print("==================",flush=True)
