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


def grow(n, initial, rules):
    initial = collections.Counter(map("".join, zip(initial[:-1], initial[1:])))

    def once(x):
        next = collections.Counter()
        for pair, count in x.items():
            middle = rules[pair]
            next[pair[0]+middle] += count
            next[middle+pair[1]] += count
        return next
    p = initial
    for _ in range(n):
        p = (once(p)
    return p

def first(a):
    print(grow(1, *a))
    print(grow(2, *a))
    stats = grow(10, *a)
    return max(stats.values()) - min(stats.values())
    pass

def second(a):
    stats = grow(40, *a)
    return max(stats.values()) - min(stats.values())

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


def parse_grid(f):
    def parse_line(l):
        return l.strip()
    return {(x,y):int(z)  for x, l in enumerate(f) for y,z in enumerate(parse_line(l))}
    pass

def parse_graph(f):
    def parse_line(l):
        return tuple(l.strip().split('-'))
    flinks = tuple(map(parse_line, f))
    rlinks = tuple((b,a) for a,b in flinks)
    links = sorted((a,b) for a,b in flinks+rlinks if b != 'start' and a != 'end')
    graph = {k:tuple(b for a,b in v) for k,v in itertools.groupby(links, key=fst)}
    graph['_big_'] = frozenset(c for c in graph if c.upper() == c)
    return graph
    pass

def parse(f):
    initial, ruless = f.read().split('\n\n')
    rules = dict(tuple(l.split(' -> ')) for l in ruless.splitlines())
    return (initial, rules)


for name in [("test_input"),
             #("test_input2"),("test_input3"),
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
