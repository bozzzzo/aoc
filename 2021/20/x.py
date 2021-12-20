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

def enhance(a):
    alg, scan = a
    ret = {}
    mx = min(map(fst, scan))
    my = min(map(snd, scan))
    Mx = max(map(fst, scan))
    My = max(map(snd, scan))
    def enhance_pix(x,y):
        return alg[sum(2**((dx+1)*3+1+2-dy)
                       for dx in range(-1,2)
                       for dy in range(-1,2)
                       if scan[(x+dx, y+dy)])]
    return collections.defaultdict(int, (((x,y),enhance_pix(x,y))
                                         for x in irange(mx-2,Mx+2)
                                         for y in irange(My+2,my-2)))

def first(a):
    show_grid(a[1])
    print()
    show_grid(enhance(a))
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
    alg, scan = f.read().split('\n\n')
    alg = alg.replace(' ','').replace('\n','')
    garbage = alg.replace('.','').replace('#','')
    assert not garbage, f">{garbage}<"
    alg = tuple(int(c=='#') for c in alg)
    scan = collections.defaultdict(int, (((x,-y), int(c=='#'))
                                        for y,l in enumerate(scan.splitlines())
                                        for x,c in enumerate(l)
                                        ))
    return alg, scan

for name in [("test_input"),
             # ("test_input2"),
             # ("test_input3"),  
             ("input")][:1
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    # pprint(a) 

    w = first(a)
    print("first", w) 
    w = second(a)
    print("second", w)

print("==================",flush=True)