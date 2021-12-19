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

def rot90(beacon, i, ax):
    for _ in range(i):
        c, (x, y) = beacon[ax], beacon[:ax]+beacon[ax+1:]
        beacon = [y, -x]
        beacon[ax:ax] = [c]
    return tuple(beacon)

#@functools.lru_cache(maxsize=None)
def gen_rot(b):
    scanner_id, beacons = b
    return ((scanner_id, tuple(rot90(rot90(rot90(beacon, i, 2), j, 1), k, 0)
                               for beacon in beacons))
            for i, j, k in [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3),
                            (0, 1, 0), (0, 2, 0), (0, 2, 1), (0, 3, 0),
                            (0, 3, 1), (1, 0, 0), (1, 0, 1), (1, 0, 2),
                            (1, 0, 3), (1, 1, 0), (1, 2, 0), (1, 2, 1),
                            (1, 3, 0), (2, 0, 0), (2, 0, 1), (2, 1, 0),
                            (2, 3, 0), (3, 0, 0), (3, 0, 1), (3, 1, 0)])

match_limit = 12

def gen_trans(a,b):
    need = set(a[1])
    seen = set()
    for i in a[1]:
        for j in b[1]:
            def translate(p):
                return tuple(x-l+o for x,l,o in zip(p,j,i))
            bp = (b[0], tuple(map(translate, b[1])))
            have = set(bp[1])
            common = need.intersection(have)
            if len(common) >= match_limit:
                key = tuple(sorted(common))
                if key not in seen:
                    yield bp, key, translate((0,0,0))
                    seen.add(key)

def align_pair(a,b):
    for rot in gen_rot(b):
        for trans in gen_trans(a,rot):
            return trans

def align(a):
    known = [(a[0], (), (0,0,0))]
    pending = a[1:]
    while pending:
        for i in range(len(pending)):
            candidate = pending[i]
            for origin, _, _ in known[::-1]:
                match = align_pair(origin, candidate)
                if match:
                   break
            else:
                continue
            known.append(match)
            del pending[i]
            print(len(known))
            break
        else:
            assert False
    return known

def first(a):
    return "skip"
    aligned = align(a)
    beacons = set(p for x in aligned for p in x[0][1])
    return len(beacons)
    pass


def manhattan(i):
    print("m", i)
    return sum(map(abs, ((a-b) for a,b in zip(i,j))))

def second(a):
    aligned = align(a)
    scanners = max(map(manhattan, itertools.combinations(((x[2] for x in aligned)), 2)))
    pprint(scanners)
    pass

def test():
    def _(a,b):
        print()
        assert a==b, f"{a}!={b}"

    pprint(list(gen_trans(("origin", [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]),
                          ("test", [(42,42,42),(44,44,44), (42,42,43)]))))
    
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
    def parse_scanner(l):
        scannerid = l[0].strip().strip('-').strip()
        beacons = tuple((tuple(map(int, b.strip().split(','))) + (0,))[:3] for b in l[1:])
        return scannerid, beacons
    return [parse_scanner(x.splitlines()) for x in f.read().split('\n\n')]

for match_limit, name in [(2, "test_input"),
             (12, "test_input2"),
             # ("test_input3"),  
             (12, "input")][:2
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
