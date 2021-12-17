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
    while x <= maxx+5 and y >= miny-5:
        yield x,y
        x += vx
        y += vy
        vx += -1 if vx > 0 else 1 if vx < 0 else 0
        vy += -1


def in_target(T, v):
    for c in launch(a,v):
        if c in T:
            return True
    return False

def show_target(a):
    return {(x,y):'T' for x in irange(*a[0]) for y in irange(*a[1])}

def show_launch(a, v, m, g=None):
    if g is None:
        g = show_target(a)
    t = tuple(launch(a, v))
    g.update((c,m) for c in t)
    return g, t

def calc_launch(a):
    (minx, maxx), (miny, maxy) = a
    # 1 + 2 + 3 + 4 + .. + t = (t+1) * t / 2
    tmin = int(math.sqrt(2 * minx))
    while tmin * (tmin + 1) < 2*minx:
        tmin += 1
    tmax = int(math.sqrt(2 * maxx))
    while tmax * (tmax + 1) < 2*maxx:
        tmax += 1
    while tmax * (tmax + 1) >= 2*maxx:
        tmax -= 1
    print(tmin, tmax)

    return((tmin, tmax),(-miny-1, -maxy-1))


def first(a):
    l = calc_launch(a)
    g = show_target(a)
    vs = tuple((vx, vy)
              for vx in irange(*l[0])
              for vy in irange(*l[1]))
    def label(i):
        l = 'abcdefghijklmnopqrstuvz1234567890'
        return l[i] if i < len(l) else '#'
    for i, v in enumerate(vs):
        g, t = show_launch(a, v, label(i), g)

    d = max(map(snd, g))

    if d < 1:
        show_grid(g)

    return d
    pass



def second(a):
    exp = sorted(tuple(map(int, v.split(','))) for v in
                 """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7""".split())
    print("exp    ", exp)

    (minx, maxx), (miny, maxy) = a

    T = show_target(a)
    vs=tuple((x,y) for x in range(1, maxx+1) for y in range(-miny+1,miny+2)
            if in_target(T, (x,y)))
    
    print("vs     ", sorted(vs))
    
    print("missing", sorted(set(exp) - set(vs)))
    print("extra  ", sorted(set(vs) - set(exp)))

    return len(vs)
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
