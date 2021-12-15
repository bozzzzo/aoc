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


def find_path(a):
    costs = {(0,0): (0, ((0,0),))} # coord : (cost, path)
    infinite = (99999999999999, ())
    active = [(0,0)]
    while active:
        active, current_active = [], active
        for current in current_active:
            base_risk, base_path = costs[current]
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                coord = (base_path[-1][0] + dx, base_path[-1][1] + dy)
                if coord not in a:
                    continue
                new_risk = base_risk + a[coord]
                current_risk, current_path = costs.get(coord, infinite)
                if new_risk < current_risk:
                    costs[coord] = (new_risk, base_path + (coord, ))
                    active.append(coord)

    return costs[max(costs)]


def first(a):
    return find_path(a)
    pass

def tile(a):
    return {
        (x * (dx + 1), y * (dy + 1)) : (v - 1 + dx + dy) % 9 + 1
        for (x,y),v in a.items()
        for dx in range(5)
        for dy in range(5)
    }


def show(a):
    mx, my = max(a)
    print("\n".join("".join(str(a[(x,y)])
                            for x in range(mx+1))
                    for y in range(my+1)))

show(tile({(0,0): 8}))

def second(a):
    return find_path(tile(a))
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
        a = parse_grid(f)
    #print(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)

print("==================",flush=True)
