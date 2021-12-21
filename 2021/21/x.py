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

def deterministic():
    while True:
        yield from range(1,101)

def game(a, die):
    die = enumerate(die, 1)
    first_pos, second_pos = a
    first_score = 0
    second_score = 0
    def move(who, pos, score):
        _, a = next(die)
        _, b = next(die)
        rolls, c = next(die)
        pos = (pos - 1 + a + b + c) % 10 + 1
        score += pos
        #print(f"{who} {a}+{b}+{c} to {pos} total {score}")
        return pos, score, rolls
    while True:
        first_pos, first_score, rolls = move("one", first_pos, first_score)
        if first_score >= 1000:
            return 0, ((first_pos, first_score, rolls), (second_pos, second_score, rolls))
        second_pos, second_score, rolls = move("two", second_pos, second_score)
        if second_score >= 1000:
            return 1, ((first_pos, first_score, rolls), (second_pos, second_score, rolls))

def first(a):
    winner, results = game(a, deterministic())
    print (winner, results)
    w_pos, w_score, w_rolls = results[winner]
    l_pos, l_score, l_rolls = results[1-winner]
    return l_score * w_rolls


def dirac(a):
    die = collections.Counter([a+b+c for a in range(1,4) for b in range(1,4) for c in range(1, 4)])
    unis = collections.Counter([(a,(0,0))])
    wins = collections.Counter()
    who = 0
    throw = 0
    while unis:
        throw += 1
        new_unis = collections.Counter()
        for (uni, uni_count), (roll, roll_count) in itertool.product(unis.items(), die.items()):
            pos = uni[0][who]
            score = uni[1][who]
            count = uni_count * roll_count

            pos = (pos - 1 + roll) % 10 + 1
            score += pos

            if score >= 21:
                wins[who] += count
            else:
                if who == 0:
                    new_uni = (pos, uni[0][1]), (score, uni[1][1])
                else:
                    new_uni = (uni[0][0], pos), (uni[1][0], score)
                new_unis[new_uni] += count

        who = 1 - who
        unis = new_unis
        if len(unis) < 100:
            print(throw, unis)

    return wins

def second(a):
    r = dirac(a)
    print(r)
    return max(r.values())



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
    return tuple(int(l.strip()) for l in f)

for name in [("test_input"),
             # ("test_input2"),
             # ("test_input3"),  
             ("input")][:2
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
