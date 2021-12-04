import functools
import itertools
import re
import collections
import pprint
import operator
import time
from dataclasses import dataclass
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


def first(a):
    pass

def second(a):
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

@dataclass
class Board:
    rows: Tuple[Tuple[int]]
    cols: Tuple[Tuple[int]]
    idx: Tuple[Tuple[int]]


@dataclass
class Bingo:
    rand: List[str]
    boards: List[Board]

def _trace(f):
    r = f.readline()
    return r
def parse_boards(f):
    while True:
        try:
            line = _trace(f).strip()
        except:
            break
        rows = []
        for _ in range(5):
            row = tuple(map(int, _trace(f).split()))
            if not row:
                return
            rows.append(tuple(row))
        cols = tuple(map(tuple, zip(*rows)))
        yield Board(rows=rows, cols=cols, idx=set(*rows))
def parse(f):
    rand = list(map(int, f.readline().strip().split(',')))
    boards = list(parse_boards(f))
    return Bingo(rand=rand, boards=boards)

for name in [("test_input"),
             ("input")][:2
                        ]:
    print("=======\n",name, flush=True)
    with open(name) as f:
        a = parse(f)
    print(a)

    first(a)
    #second(a)

print("==================",flush=True)
