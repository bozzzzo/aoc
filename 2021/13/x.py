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


def show(dots):
    mx, my = max(dots)
    for y in irange(0, my):
        print ("".join('#' if (x,y) in dots else '.' for x in irange(0,mx)))

def fold(dots, folds):
    for direction, loc in folds:
        if direction == 'x':
            dots = fold_x(dots, loc)
        elif direction == 'y':
            dots = fold_y(dots, loc)
        else:
            assert False, direction

def fold_y(dots, loc):
    mx, my = max(dots)
    assert not any((x,loc) in dots for x in irange(0,mx)), str(loc)
    return set((x, y if y < loc else my - y) for x, y in dots)


def first(a):
    dots, folds = a
    dots1 = fold(dots, folds[:1])
    show(dots1)
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
    dotss, foldss = f.read().split('\n\n')
    dots = set((tuple(map(int, l.strip().split(','))) for l in dotss.splitlines()))
    folds = [tuple(l.split()[-1].split('=')) for l in foldss.splitlines()]
    return (dots, folds)


for name in [("test_input"),
             #("test_input2"),("test_input3"),
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
