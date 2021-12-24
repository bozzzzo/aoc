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

def monad(a):
    zero = '0'
    state = dict(x=zero, y=zero, z=zero, w=zero)
    def evl(x):
        if isinstance(x, int):
            return x
        else:
            return state[x]
    for op, reg, *_arg in a:
        arg = evl(_arg[0]) if _arg else None
        if op == 'inp':
            state[reg] = 'next(s)'
        elif op == 'add':
            state[reg] = f'({state[reg]} + {arg})'
        elif op == 'mul':
            state[reg] = f'({state[reg]} * {arg})'
        elif op == 'div':
            state[reg] = f'({state[reg]} // {arg})'
        elif op == 'mod':
            state[reg] = f'({state[reg]} % {arg})'
        elif op == 'eql':
            state[reg] = f'int({state[reg]} == {arg})'
        else:
            assert False, str((op, reg, arg))

    print(state)

    z = compile(state['z'], 'monad', 'eval')

    def run(s):
        return eval(z)

    return run


def first(a):
    f = monad(a)
    for model in itertools.product(*([range(9,0,-1)] * 14)):
        if f(iter(model)) == 0:
            return model
    return None
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
    def parse_insn(l):
        return tuple(map(strint, l.split()))
    return tuple(map(parse_insn, f.splitlines()))
    pass


for name in [("test_input"),
             #("test_input2"),
             #("test_input3"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        f = f.read()
    a = parse(f)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)

print("==================",flush=True)