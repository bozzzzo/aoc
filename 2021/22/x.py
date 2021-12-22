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

def overlaps(r1, r2):
    assert r1.step == 1
    assert r2.step == 1
    if r1.stop <= r2.start: return False
    if r2.stop <= r1.start: return False
    return True

def inside(r1, r2):
    assert r1.step == 1
    assert r2.step == 1
    return r1.start >= r2.start and r1.stop <= r2.stop

def partition(r1, r2):
    "return all parts of r1 chopped by r2"
    if r1.start <= r2.start:
        if r1.stop <= r2.start:
            yield r1
        elif r1.stop <= r2.stop:
            yield range(r1.start, r2.start)
            yield range(r2.start, r1.stop)
        else:
            yield range(r1.start, r2.start)
            yield r2
            yield range(r2.stop, r1.stop)
    else:
        if r2.stop <= r1.start:
            yield r1
        elif r2.stop <= r1.stop:
            yield range(r1.start, r2.stop)
            yield range(r2.stop, r1.stop)
        else:
            yield r1


def common(r1, r2):
    assert overlaps(r1, r2)
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))

class Cuboid:
    def __init__(self, coords):
        self.coords = tuple(coords)
    def __repr__(self):
        return type(self).__name__ + str(self.coords)

    @property
    def volume(self):
        return functools.reduce(operator.mul, map(len, self.coords))

    def overlaps(self, other):
        return all(overlaps(a,b) for a,b in zip(self.coords, other.coords))

    def inside(self, other):
        return all(inside(a,b) for a,b in zip(self.coords, other.coords))

class On(Cuboid):
    def __add__(self, other):
        assert isinstance(self, On)
        if isinstance(other, On):
            if not self.overlaps(other):
                return ((self,), True)
            if self.inside(other):
                return ((), True)
            elif other.inside(self):
                return ((self,), False)
            else:
                return (tuple(self.without(other)), True)
        elif isinstance(other, Off):
            if not self.overlaps(other):
                return ((self,), True)
            elif self.inside(other):
                return ((), True)
            else:
                return (tuple(self.without(other)), True)
        else:
            assert False, str(other)

    def without(self, other):
        cubes = tuple(On(c) for c in itertools.product(
            *(partition(a,b) for a,b in zip(self.coords, other.coords))))
        print("without", cubes)
        for cube in cubes:
            if not cube.inside(other) and cube.volume:
                yield cube


class Off(Cuboid):
    pass

class Reactor:
    def __init__(self, *contents):
        self.contents = tuple(*contents)

    @property
    def volume(self):
        return sum(x.volume for x in self.contents)

    def __add__(self, other):
        new_cuboids = []
        for i, cuboid in enumerate(self.contents):
            parts, proceed = cuboid + other
            new_cuboids.extend(parts)
            if not proceed:
                new_cuboids.extend(self.contents[i+1:])
                break
        else:
            if isinstance(other, On):
                new_cuboids.append(other)


        return type(self)(new_cuboids)

    def __repr__(self):
        return repr(self.contents)


def first(a):
    core = Cuboid([range(-50,51)]*3)
    print("core", core)
    r = Reactor()
    for c in a:
        print("c", c)
        r = r + c
        print("r", r.volume)
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
    states = dict(off=Off,on=On)
    def cuboid(l):
        state, d = l.split()
        d = dict((i, tuple(map(int, x.split('..'))))
                 for i, x in [c.split('=') for c in d.split(',')])
        return states[state](srange(*d[i]) for i in "xyz")
    return tuple(cuboid(l.strip()) for l in f)

for name in [("test_input"),
             # ("test_input2"),
             # ("test_input3"),  
             ("input")][:1
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
