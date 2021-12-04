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


def first(a):
    states = a.states()
    for number in a.rand:
        states = [state.board.call(state, number) for state in states]
        winning = sorted((state.score(), state) for state in states if state.winning())
        if winning:
            return winning[-1]
    pass

def second(a):
    states = a.states()
    for number in a.rand:
        states = [state.board.call(state, number) for state in states]
        not_winning = [state for state in states if not state.winning()]
        if not_winning:
            states = not_winning
        else:
            winning = sorted((state.score(), state) for state in states if state.winning())
            return winning[-1]
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

    def call(self, state, n):
        if n not in self.idx:
            return state
        if n in state.called:
            return state
        def call_rows(rows, counts, n):
            return tuple(count+1 if n in row else count
                         for row, count in zip(rows, counts))
        rows = call_rows(self.rows, state.rows, n)
        cols = call_rows(self.cols, state.cols, n)
        called = state.called + (n,)
        return replace(state,
                       rows=rows,
                       cols=cols,
                       called=called)


@dataclass
class BoardState:
    board: Board
    called: Tuple[int] = field(default=())
    rows: Tuple[int] = field(default=(0,0,0,0,0))
    cols: Tuple[int] = field(default=(0,0,0,0,0))

    def winning(self):
        return 5 in self.rows or 5 in self.cols

    def score(self):
        missing = sum(set(self.board.idx) - set(self.called))
        return missing * self.called[-1]

@dataclass
class Bingo:
    rand: List[str]
    boards: List[Board]

    def states(self):
        return [BoardState(board) for board in self.boards]

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
        yield Board(rows=rows, cols=cols, idx=set(itertools.chain(*rows)))

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
    #print(a)

    w = first(a)
    print("first", w)
    w = second(a)
    print("second", w)
    #second(a)

print("==================",flush=True)
