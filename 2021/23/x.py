import functools
import itertools
import re
import collections
import pprint
import operator
import json
import time
import math
import heapq
from dataclasses import dataclass, replace, field
import numpy as np
from typing import *
from pprint import pprint

import numpy as np

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

def srange(a,b):
    return irange(a,b) if a < b else irange(b,a)

targets = dict((c, tuple((x*2 + 1, y) for y in (2,3))) for x, c in enumerate('ABCD', 1))
costs = dict(A=1,
             B=10,
             C=100,
             D=1000)

def moves(a, cost):
    going = tuple(((x,y), c) for (x,y), c in a.items() if c in 'ABCD' and a.get((x,y-1),' ') not in 'ABCD' and y > 1)
    destinations = (1,2,4,6,8,10,11)
    for (sx, sy), c in going:
        ny = 1
        for nx in destinations:
            if a[(nx,ny)] != '.':
                continue
            if any(a.get((x,1),' ') in 'ABCD' for x in irange(sx,nx)):
                continue
            b = a.copy()
            b[(sx,sy)] = '.'
            b[(nx,ny)] = c
            exp = abs(ny-sy) + abs(nx-sx)
            yield b, cost + exp * costs[c]

    coming = tuple(((x,y), c)
                   for (x,y), c in a.items()
                   if c in 'ABCD' and
                   a.get((x,y-1),' ') not in 'ABCD' and
                   all(a[t] in (c, '.') for t in targets[c]))
    for (sx,sy), c in coming:
        for nx, ny in targets[c]:
            if sx == nx:
                continue
            if a.get((nx,ny+1)) == '.':
                continue
            if any(a.get((x,1), ' ') in 'ABCD' for x in irange(sx,nx)):
                continue
            b = a.copy()
            b[(sx,sy)] = '.'
            b[(nx,ny)] = c
            exp = abs(ny-sy) + abs(nx-sx)
            yield b, cost + exp * costs[c]

def all_moves(start, start_key, _seen=set()):
    for move, cost in moves(a, 0):
        move_key = render_grid(move)
        yield (move_key, start_key), cost
        if move_key not in _seen:
            _seen.add(move_key)
            yield from all_moves(move, move_key)

def first(a):
    start = a
    start_key = render_grid(start)
    graph = dict(all_moves(start, start_key))

    end = a.copy()
    end.update((x, c) for c, t in targets.items() for x in t)
    end_key = render_grid(end)

    costs = dict([(end_key, 0)] + [(k2, 99999999999999999999999999999) for k1,k2 in graph])
    prev = dict()
    unvisited = set(costs)
    assert start_key in unvisited

    with open(f"{name}.dot", "w") as fd:
        def lbl(k):
            k=k.replace('\n',',')
            return f'"{k}"'
        fd.write("digraph {")
        fd.writelines(f'{lbl(k)} [label="."];\n'
                      for _,k in graph)
        fd.write(f'{lbl(start_key)} [label="start"];\n')
        fd.write(f'{lbl(end_key)} [label="end"];\n')
        fd.writelines(f'{lbl(k1)} -> {lbl(k2)} [label="{c}"];\n'
                      for (k1,k2),c in graph.items())
        fd.write("}")

    while unvisited:
        cost, u = min((costs[x], x) for x in unvisited)
        unvisited.remove(u)
        
        for (x, v), c in graph.items():
            if x != u or v not in unvisited:
                continue
            alt = cost + c
            if alt < costs[v]:
                costs[v] = alt
                prev[v] = u

    return costs[start_key]


    print(len(graph))
    print('----------------------')
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
    print(render_grid(a))

def render_grid(a):
    mx = min(map(fst, a))
    my = min(map(snd, a))
    Mx = max(map(fst, a))
    My = max(map(snd, a))
    return ("\n".join("".join(str(a.get((x,y), '_'))
                            for x in irange(mx,Mx))
                    for y in irange(my,My)))

def parse_grid(f):
    def parse_line(l):
        return l
    return {(x,y):z  for y, l in enumerate(f) for x,z in enumerate(parse_line(l)) if z not in "# \n" and (y != 1 or x not in (3,5,7,9))}
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
    pass

# test_input
#############
#.. . . . ..#
###B#C#B#D###
  #A#D#C#A#
  #########



#############
#.. . . . ..#
###C#B#D#D###
  #B#C#A#A#
  #########


for name in [("test_input"),
             # ("test_input2"),
             # ("test_input3"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse_grid(f)
    show_grid(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)

print("==================",flush=True)
