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


def interesting1(a, big, path, next):
    return next in big or next not in path

def interesting2(a, big, path, next):
    c = collections.Counter(path + (next,))
    x = [v for k,v in c.items() if k not in big and v > 1]
    #print(path, next, c, x)
    return sum(x) <= 2

def step(a, paths, interesting):
    new_paths = set()
    new_done_paths = set()
    big = a['_big_']
    for path in paths:
        #print(path)
        cave = path[-1]
        for next in a[cave]:
            if next == 'end':
                new_done_paths.add(path)
            elif not interesting(a, big, path, next):
                pass
            else:
                new_path = path + (next,)
                new_paths.add(new_path)

    return new_paths, new_done_paths


def walk(a, interesting):
    paths = set([('start',)])
    done = set()
    while paths:
        new_paths, new_done = step(a, paths, interesting)
        #print(paths, done)
        #print(new_paths, new_done)
        done |= new_done
        paths = new_paths
    return done

def first(a):
    paths = walk(a, interesting1)
    return len(paths)
    pass


def second(a):
    paths = walk(a, interesting2)
    return len(paths)
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

def parse(f):
    def parse_line(l):
        return tuple(l.strip().split('-'))
    flinks = tuple(map(parse_line, f))
    rlinks = tuple((b,a) for a,b in flinks)
    links = sorted((a,b) for a,b in flinks+rlinks if b != 'start' and a != 'end')
    graph = {k:tuple(b for a,b in v) for k,v in itertools.groupby(links, key=fst)}
    graph['_big_'] = frozenset(c for c in graph if c.upper() == c)
    return graph
    pass

for name in [("test_input"),
             ("test_input2"),("test_input3"),
             ("input")][:1
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    #print(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)

print("==================",flush=True)
