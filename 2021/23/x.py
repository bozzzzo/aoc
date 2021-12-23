import functools
import itertools
import re
import collections
import pprint
import operator
import json
import time
import math
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


def first(a):
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
    ui = {0:'.',1:'#'}
    print("\n".join("".join(str(ui.get(a.get((x,y),0), ' '))
                            for x in irange(mx,Mx))
                    for y in irange(my,My)))

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
    pass

# test_input
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

#############
#...........#
###C#B#D#D###
  #B#C#A#A#
  #########

x = collections.Counter(dict(
 ('d', 2),
 ('a', 3),
 ('d', 3),
 ('d', 4),
 ('a', 3),
 ('c', 7),
 ('b', 2),
 ('c', 5),
 ('b', 3),
 ('b', 5),
 ('a', 7),
 ('a', 8),
))
print(x)
cost = dict(a=1, b=10, c=100, d=1000)
print(sum(cost[k]*v for k,v in x.items()))

for name in [("test_input"),
             # ("test_input2"),
             # ("test_input3"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    pprint(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)

print("==================",flush=True)
