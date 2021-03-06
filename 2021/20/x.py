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

def enhance(alg, scan):
    ret = {}
    mx = min(map(fst, scan))
    my = min(map(snd, scan))
    Mx = max(map(fst, scan))
    My = max(map(snd, scan))
    def enhance_pix(x,y):
        area = collections.defaultdict(int, (((dx,dy), scan[(x+dx-1, y+dy-1)])
                                             for dx in range(3)
                                             for dy in range(3)))
        #print(x,y)
        #show_grid(area)
        bits = tuple(area[(dx,dy)] for dy in range(3) for dx in range(3))
        #print(bits)
        return functools.reduce(lambda x,y: x*2+y, bits)

    #print(enhance_pix(2,2))
    #print("======")
    return collections.defaultdict(lambda:alg[scan[(mx-1,my-1)]*511], (((x,y),alg[enhance_pix(x,y)])
                                                   for x in irange(mx-3,Mx+3)
                                                   for y in irange(my-3,My+3)))

def first(a):
    alg, scan = a
    #print("input"); show_grid(scan)
    scan = enhance(alg, scan)
    #print("enhance 1"); show_grid(scan)
    scan = enhance(alg, scan)
    #print("enhance 2"); show_grid(scan)
    return sum(scan.values())
    pass 



def second(a):
    alg, scan = a
    for _ in range(50):
        scan = enhance(alg, scan)
    return sum(scan.values())
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
    alg, scan = f.read().split('\n\n')
    alg = alg.replace(' ','').replace('\n','')
    garbage = alg.replace('.','').replace('#','')
    assert not garbage, f">{garbage}<"
    alg_ = tuple(int(c=='#') for c in alg)
    assert alg == "".join(".#"[x] for x in alg_)
    scan = collections.defaultdict(int, (((x,y), int(c=='#'))
                                        for y,l in enumerate(scan.splitlines())
                                        for x,c in enumerate(l)
                                        ))
    return alg_, scan

for name in [("test_input"),
             # ("test_input2"),
             # ("test_input3"),  
             ("input")][:2
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
