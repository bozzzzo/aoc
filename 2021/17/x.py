import functools
import itertools
import re
import collections
import pprint
import operator
import time
import math
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


def launch(a, v):
    x, y = 0,0
    vx, vy = v
    (minx, maxx), (miny, maxy) = a
    while x <= maxx and y > miny:
        yield x,y
        x += vx
        y += vy
        vx += -1 if vx > 0 else 0
        vy += -1


def show_launch(a, v):
    g = {(x,y):'T' for x in irange(*a[0]) for y in irange(*a[1])}
    t = tuple(launch(a, v))
    
    g.update((c,'#') for c in t)
    print(a, v)
    show_grid(g)
    return t

def calc_launch(a):
    (minx, maxx), (miny, maxy) = a
    # 1 + 2 + 3 + 4 + .. + t = (t+1) * t / 2
    tmin = int(math.sqrt(2 * minx))
    while tmin * (tmin + 1) < minx:
        tmin += 1
    tmax = int(math.sqrt(2 * maxx))
    while tmax * (tmax + 1) <= maxx:
        tmax += 1
    while tmax * (tmax + 1) > maxx:
        tmax -= 1
    print(tmin, tmax)

    return(tmin+1,-miny-1)
    


def first(a):
    show_launch(a, calc_launch(a))
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
    mx = min(map(fst, a))
    my = min(map(snd, a))
    Mx = max(map(fst, a))
    My = max(map(snd, a))
    print("\n".join("".join(str(a.get((x,y), ' '))
                            for x in irange(mx,Mx))
                    for y in irange(My,my)))

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
