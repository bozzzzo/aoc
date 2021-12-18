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

class Num:
    def __init__(self, n):
        self.n = n

    def _link(self, p):
        self.p = p

    @property
    def d(self):
        return -1

    def copy(self):
        return Num(self.n)

    @property
    def max(self):
        return self.n

    @property
    def magnitude(self):
        return self.n

    def __str__(self):
        return str(self.n)

class Pair:
    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.p = None

    def _link(self, p):
        self.p = p

    @property
    def d(self):
        return 1+max(self.l.d, self.r.d)

    @property
    def max(self):
        return max(self.l.max, self.r.max)

    @classmethod
    def make(cls, a):
        return cls._make(*[Num(v) if isinstance(v, int) else cls.make(v) for v in a])

    @classmethod
    def _make(cls, l, r):
        p = cls(l, r)
        p.l._link(p)
        p.r._link(p)
        return p

    def copy(self):
        return self._make(self.l.copy(), self.r.copy())

    def __add__(self, other):
        return self._make(self.copy(), other.copy()).reduce()

    def reduce(self):
        p = self
        while True:
            if p.d >= 4:
                p = p.explode()
                continue
            if p.max >= 10:
                p = p.split()
                continue
            return p

    def prevnumber(self):
        p = self
        while p.p is not None and p.p.l is p:
            p = p.p
        if p.p is None:
            return None
        p = p.p.l
        while isinstance(p, Pair):
            p = p.r
        return p

    def nextnumber(self):
        p = self
        while p.p is not None and p.p.r is p:
            p = p.p
        if p.p is None:
            return None
        p = p.p.r
        while isinstance(p, Pair):
            p = p.l
        return p

    def explode(self):
        p = self
        prev = self
        while isinstance(p, Pair):
            prev, p = p, p.l if p.l.d >= p.r.d else p.r
        p = prev
        assert isinstance(p.l, Num)
        assert isinstance(p.r, Num)
        pn = p.prevnumber()
        if pn is not None:
            pn.n += p.l.n
        nn = p.nextnumber()
        if nn is not None:
            nn.n += p.r.n
        z = Num(0)
        pp = p.p
        if pp.l is p:
            pp.l = z
        elif pp.r is p:
            pp.r = z
        else:
            assert False
        z._link(pp)
        print("explode", p, pn.p, z.p, nn.p)
        return self

    def split(self):
        p = self
        while isinstance(p, Pair):
            p = p.l if p.l.max >= 10 else p.r
        pp = p.p
        assert isinstance(p, Num)
        np = self.make([p.n//2, (p.n+1)//2])
        if pp.l is p:
            pp.l = np
        elif pp.r is p:
            pp.r = np
        else:
            assert False
        np._link(pp)
        print("split", p, np)
        return self

    @property
    def magnitude(self):
        return 3*self.l.magnitude + 2*self.r.magnitude

    def __str__(self):
        return f"<{self.l}, {self.r}>"

def first(a):
    s = functools.reduce(operator.add, a)
    print(s)
    return s.magnitude
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
    return [Pair.make(json.loads(l)) for l in f]


for name in [("test_input"),
             #("test_input2"),("test_input3"),
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
