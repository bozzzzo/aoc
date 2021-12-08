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

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""
digits = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}
digits_ = {v:k for k,v in digits.items()}

bylen = {k:tuple(v) for k,v in itertools.groupby(sorted(digits_, key=len), key=len)
}


print(bylen)

def decode0(l):
    samples, result = l
    return sum((len(r) in (2,3,4,7) for r in result))

def first(a):
    n = sum(map(decode0, a))
    return n
    pass

def decode1(l):
    letters = 'abcdefgh'
    samples, result = l
    sbl = {k:tuple(map(set,v)) for k,v in itertools.groupby(sorted(samples, key=len), key=len)
           }
    print(sbl)
    lone = 2
    lseven = 3
    lfour = 4
    leight = 7
    scf = sbl[lone][0]
    sacf = sbl[lseven][0]
    sa = sacf - scf
    sbcdf = sbl[lfour][0]
    sbd = sbcdf - scf
    sd = sbl[leight][0] - [d for d in sbl[6] if not sbd.issubset(d)][0]
    sb = sbd - sd
    sc = sbl[leight][0] - [d for d in sbl[6] if sd.issubset(d) and not scf.issubset(d)][0]
    sf = scf - sc
    sg = [d for d in sbl[5] if scf.issubset(d)][0] - sacf - sd
    se = [d for d in sbl[5] if not sf.issubset(d) and sc.issubset(d)][0] - sa - sc - sd - sg
    print('a', sa, 'bd', sbd, 'd', sd, 'c', sc, 'f', sf, 'g', sg, 'e', se)
    
    
    return 0
    pass


def second(a):
    n = tuple(map(decode1, a))
    print(n)
    return sum(n)
    pass

def test():
    pass


test()

def strint(x):
    try:
        return int(x)
    except:
        pass
    return x


def parse(f):
    def parse_line(l):
        samples, result = l.split('|')
        return (tuple("".join(sorted(s)) for s in samples.strip().split()),
                tuple("".join(sorted(r)) for r in result.strip().split()))
    return tuple(map(parse_line, f))
    pass

for name in [("test_input"),
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
