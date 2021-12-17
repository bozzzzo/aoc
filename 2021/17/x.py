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


def launch(a, vx, vy):
    x,y = 0,0
    (minx, maxx), (miny, maxy) = a
    while x <= maxx and y > miny:
        yield x,y
        x += vx
        y += vy
        vx += -1 if vx > 0 else 1 if vx < 0 else 0
        vy += -1


def show_launch(a, vx, vy):
    g = {(x,y):'T' for x in irange(*a[0]) for y in irange(*a[1])}
    t = tuple(launch(a, vx, vy))
    g.update((c,'#') for c in t)
    show_grid(g)
    return t

def first(a):
    show_launch(a, 5,5)
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


def show_grid(a):
    mx, my = max(a)
    print("\n".join("".join(str(a.get((x,y), ' '))
                            for x in range(mx+1))
                    for y in range(my+1)))

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
    l = tuple(tuple(map(int, x.split('=')[1].split('..'))) for x in f.readline().split(','))
    return l 

for name in [("test_input"),
             #("test_input2"),("test_input3"),
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
