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

@dataclass
class Insn:
    ver: int
    typ: int

@dataclass
class Lit(Insn):
    val: int

@dataclass
class Op(Insn):
    arg: List[Insn]

def bits(s, n):
    data, off = s
    return int(data[:n], 2), (data[n:], off + n)

def parse_packet(s):
    ver, s = bits(s, 3)
    typ, s = bits(s, 3)
    if typ == 4:
        return parse_lit(s, ver, typ)
    else:
        return parse_op(s, ver, typ)

def parse_lit(s, ver, typ):
    flag, s = bits(s, 1)
    result, s = bits(s, 3)
    while flag:
        flag, s = bits(s, 1)
        part, s = bits(s, 3)
        result = result * 8 + part
    return Lit(ver, typ, result), s

def parse_op(s, ver, typ):
    tid, s = bits(s, 1)
    arg = []
    if tid == 0:
        tlib, s = bits(s, 15)
        pos = s
        def stop(s, arg):
            s[1] >= tlib + pos[1]
    elif tid == 1:
        np, s = bits(s, 11)
        def stop(s, arg):
            len(arg) == np
    while not stop(s, arg):
        op, s = parse_packet(s)
        arg.append(op)
    return Op(ver, typ, arg)


def versum(p):
    if isinstance(p, Lit):
        return p.ver
    if isinstance(p, Op):
        return p.ver + sum(map(versum, p.arg))
    assert(False)

def first(a):
    return [(versum(p), p) for p in (parse_packet((p,0)) for p in a)]
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
    mx, my = max(a)
    print("\n".join("".join(str(a[(x,y)])
                            for x in range(mx+1))
                    for y in range(my+1)))

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
    return tuple(bin(int(l.strip(), 16))[2:] for l in f)


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
