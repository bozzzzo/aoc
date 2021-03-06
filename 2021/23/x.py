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
import sys

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

targets = dict((c, tuple((x*2 + 1, y) for y in (2,3,4,5))) for x, c in enumerate('ABCD', 1))
costs = dict(A=1,
             B=10,
             C=100,
             D=1000)

def going_moves(a, cost):
    depth = max(y for (x,y), c in a.items() if c in 'ABCD')
    going = tuple(((x,y), c)
                  for (x,y), c in a.items()
                  if
                  y > 1 and
                  c in 'ABCD' and
                  a.get((x,y-1),' ') not in 'ABCD'
                  )
    destinations = (1,2,4,6,8,10,11)
    for (sx, sy), c in going:
        ny = 1
        for nx in destinations:
            if sx == targets[c][0][0]:
                if all(a[(sx,y)] == c for y in irange(sy, depth)):
                    continue
            if a[(nx,ny)] != '.':
                continue
            if any(a.get((x,1),' ') in 'ABCD' for x in irange(sx,nx)):
                continue
            b = a.copy()
            b[(sx,sy)] = '.'
            b[(nx,ny)] = c
            exp = abs(ny-1) + abs(sy-1) + abs(nx-sx)
            yield b, cost + exp * costs[c]

def coming_moves(a, cost):
    depth = max(y for (x,y), c in a.items() if c in 'ABCD')
    coming = tuple(((x,y), c)
                   for (x,y), c in a.items()
                   if c in 'ABCD' and
                   a.get((x,y-1),' ') not in 'ABCD' and
                   all(a[t] in (c, '.') for t in targets[c] if t[1] <= depth) and
                   ( y == 1 or
                     x != targets[c][0][0]))
    for (sx,sy), c in coming:
        for nx, ny in targets[c]:
            if ny > depth:
                continue
            if sx == nx:
                continue
            if a.get((nx,ny+1)) == '.':
                continue
            if a.get((nx,ny)) != '.':
                continue
            if any(a.get((x,1), ' ') in 'ABCD' for x in irange(sx,nx) if x != sx):
                continue
            b = a.copy()
            b[(sx,sy)] = '.'
            b[(nx,ny)] = c
            exp = abs(ny-1) + abs(sy-1) + abs(nx-sx)
            yield b, cost + exp * costs[c]

def moves(a, cost):
    yield from going_moves(a, cost)
    yield from coming_moves(a, cost)

def all_moves(start, start_key, *, _seen, d):
    if start_key not in _seen:
        _seen.add(start_key)
        for i, (move, cost) in enumerate(moves(start, 0)):
            # print (' ' * d, i, "   ", cost)
            # show_grid(move, prefix=' '*d)
            move_key = render_grid(move)
            yield (move_key, start_key), cost
            yield from all_moves(move, move_key, _seen=_seen, d=d+1)
            # print(' '*d, "--")

def first(a):
    sys.setrecursionlimit(100000)
    depth = max(y for (x,y), c in a.items() if c in 'ABCD')

    print("start")
    start = a
    start_key = render_grid(start)

    print("end")
    end = a.copy()
    end.update((x, c) for c, t in targets.items() for x in t if x[1] <= depth)
    end_key = render_grid(end)

    print("prev")
    prev = end.copy()
    prev[1,1], prev[5,2] = prev[5,2], prev[1,1]
    prev_key = render_grid(prev)

    com = list(coming_moves(prev, 0))
    assert com
    assert len(com) == 1

    print("========================================")
    seen = set()
    graph = dict(all_moves(start, start_key, _seen=seen, d=0))
    print("graph", len(graph))
    assert start_key in seen
    assert end_key in seen

    # assert any(end_key == k2 for k1,k2 in graph)
    assert any(end_key == k1 for k1,k2 in graph)
    print("========================================")

    dist = dict(
        [(k2, 99999999999999999999999999999) for k1,k2 in graph] +
        [(k1, 99999999999999999999999999999) for k1,k2 in graph] +
        [(end_key, 0)])
    prev = dict()
    Q = set(dist)
    assert start_key in Q
    assert end_key in Q
    assert start_key != end_key

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

    neighbors = collections.defaultdict(set)
    for k1,k2 in graph:
        neighbors[k1].add(k2)

    assert neighbors[end_key]
    assert start_key not in neighbors[end_key]

    mindist = list((dist[q], q) for q in Q)
    heapq.heapify(mindist)

    print("search in ", len(Q))
    while Q:
        while True:
            cost, u = heapq.heappop(mindist)
            if u in Q:
                break
        Q.remove(u)
        assert cost == dist[u]
        print(len(Q), end='\r        ', flush=True)
        if u == end_key:
            assert cost == 0
            print("found end", cost, "next", neighbors[u])
        if u == start_key:
            print("found start", cost)
        for v in neighbors[u].intersection(Q):
            alt = dist[u] + graph[(u,v)]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(mindist, (alt, v))

    print('done             ')

    def show_solution():
        x = start_key
        i = 0
        while x != end_key:
            print(f"==== step {i} {dist[x]} {graph[(prev[x],x)]}")
            print(x)
            x = prev[x]
    

    return dist[start_key]


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


def show_grid(a, *, prefix=''):
    print(render_grid(a, prefix=prefix))

def render_grid(a, *, prefix=''):
    mx = min(map(fst, a))
    my = min(map(snd, a))
    Mx = max(map(fst, a))
    My = max(map(snd, a))
    return prefix + (("\n"+prefix).join("".join(str(a.get((x,y), '_'))
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
        f = f.readlines()
    a = parse_grid(f)
    show_grid(a)

    w = first(a)
    print("first", w)
    f[3:3] = [
        '  #D#C#B#A#',
        '  #D#B#A#C#'
    ]
    print(f)
    a = parse_grid(f)
    show_grid(a)
    w = first(a)
    print("second", w)

print("==================",flush=True)
