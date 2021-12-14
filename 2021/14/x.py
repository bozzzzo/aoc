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


def grow_first(n, initial, rules):
    def once(x):
        yield x[0]
        for i in range(0,len(x)-1):
            yield rules[x[i:i+2]]
            yield x[i+1]
    p = initial
    for _ in range(n):
        p = "".join(once(p))
    return p, collections.Counter(sorted(p))


def grow_second(n, initial, rules):

    def once(x):
        next = collections.Counter()
        for pair, count in x.items():
            middle = rules[pair]
            next[pair[0]+middle] += count
            next[middle+pair[1]] += count
        return next

    p = collections.Counter(map("".join, zip(initial[:-1], initial[1:])))
    for _ in range(n):
        p = once(p)

    stats = collections.Counter()
    for pair, v in p.items():
        stats[pair[0]] += v
        stats[pair[1]] += v
    return stats

def first(a):
    print(grow_first(1, *a))
    print(grow_first(2, *a))
    _, stats = grow_first(10, *a)
    return max(stats.values()) - min(stats.values())
    pass

def second(a):
    print(grow_first(1, *a))
    print(grow_second(1, *a))
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
