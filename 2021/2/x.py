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
    c = functools.reduce(operator.add, a)
    dep = c['down'] - c['up']
    dist = c['forward']
    print(dep, dist, dep*dist)


def second(a):
    def ops():
        def up(x, y):
            aim, depth, distance = x
            aim -= y
            return aim, depth, distance
        def down(x, y):
            aim, depth, distance = x
            aim += y
            return aim, depth, distance
        def forward(x, y):
            aim, depth, distance = x
            distance += x
            depth += aim * x
            return aim, depth, distance
        return locals()
    def dispatch(x, ys, ops=ops()):
        for op, y in ys.items():
            x = ops[op](x, y)
        return x
    aim, depth, distance = functools.reduce(dispatch, a, (0,0,0))
    print (aim, depth, distance, depth*distance)

def test():
    pass


test()

def parse(x):
    x = x.split()
    return collections.Counter({x[0]: int(x[1])})

for name in [("test_input"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = tuple(parse(l.strip()) for l in f)
    #print(a)

    second(a)

print("==================",flush=True)
