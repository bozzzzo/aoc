import functools
import itertools
import re
import collections
import pprint
import operator
import time
from dataclasses import dataclass
import numpy as np
from pprint import pprint

def fst(x):
    return x[0]

def snd(x):
    return x[1]

def dbg(*x, **y):
    # print(*x, **y)
    pass


def first(a):
    bits = tuple(map(sum, map(lambda x: map(int,x), zip(*a))))
    l = len(a)/2
    gamma = int(''.join('1' if b > l else '0' if b < l else '=' for b in bits), 2)
    epsilon = int(''.join('1' if b < l else '0' if b > l else '=' for b in bits), 2)
    print(l, tuple(bits), gamma, epsilon, gamma*epsilon)
    

def second(a):
    def count(a, i):
        return sum(int(b[i]) for b in a)
    l = len(a)/2
    def O(a, i):
        #print(a, i)
        if len(a) == 1:
            return int(a[0], 2)
        c = count(a, i)
        l = (len(a) + 1) // 2
        bit = '1' if c >= l else '0'
        return O([b for b in a if b[i] == bit], i+1)
    def CO2(a, i):
        #print(a, i)
        if len(a) == 1:
            return int(a[0], 2)
        c = count(a, i)
        l = (len(a) + 1) // 2
        bit = '1' if c < l else '0'
        return CO2([b for b in a if b[i] == bit], i+1)
    o = O(a, 0)
    co2 = CO2(a, 0)
    print(o, co2, o * co2)

def test():
    pass


test()

def strint(x):
    try:
        return int(x)
    except:
        pass
    return x

def parse(x):
    return x

for name in [("test_input"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = tuple(parse(l.strip()) for l in f)
    #print(a)

    #first(a)
    second(a)

print("==================",flush=True)
