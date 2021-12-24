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
    zero = 0

    digit = 0
    indent = "  "
    code = ['def loop():',
            '  x0=y0=z0=w0=0'
            ]
    ret = []
    for op, _reg, *_arg in a:
        arg = _arg[0] if _arg else 0
        arg = arg if isinstance(arg, int) else arg+str(digit)
        reg = _reg + str(digit)
        code.append(f"{indent}# {op} {_reg}, {_arg}")
        if op == 'inp':
            digit += 1
            it = _reg + str(digit)
            code.append(f'{indent}for {it} in range(9,0,-1):')
            ret.append(it)
            indent += "  "
            code.extend(f'{indent}{r}{digit}={r}{digit-1}' for r in 'xyzw' if r != _reg)
            #code.append('print(">>", x,y,z,w)')
        elif op == 'add':
            code.append(f'{indent}{reg} += {arg}')
        elif op == 'mul':
            code.append(f'{indent}{reg} *= {arg}')
        elif op == 'div':
            code.append(f'{indent}{reg} //= {arg}')
        elif op == 'mod':
            code.append(f'{indent}{reg} %= {arg}')
        elif op == 'eql':
            code.append(f'{indent}{reg} = int({reg} == {arg})')
        else:
            assert False, str((op, reg, arg))

    code.append(f'{indent}if z{digit}: continue')
    def mul(ret):
        if len(ret) == 1:
            return ret[0]
        else:
            return f'({mul(ret[:-1])} * 10 + {ret[-1]})'
    code.append(f'{indent}# {ret}')
    code.append(f'{indent}ret = {mul(ret)}')
    code.append(f'{indent}return ret')
    code.append('ret=loop()')

    code = "\n".join(code)
    print(code)

    prog = compile(code, 'monad', 'exec')
    print(prog)

    def run():
        state=dict(ret=None)
        eval(prog, globals(), state)
        return state['ret']

    return run

class Lazy:
    pass

class Const:
    def __init__(self, value):
        self.value = value

    @property
    def const(self):
        return True

class Var(Lazy):
    def __init__(self, i, value=range(1,10)):
        self.listeners = []
        self.i = i
        self._value = value

    @property
    def const(self):
        return isinstance(self._value, int)

    def set(self, value):
        self.value = value
        for l in listeners:
            l.recalc()

    def __repr__(self):
        return f"Var({self.i},{self._value})"


class Op(Lazy):
    def __init__(self, *ops):
        self.listeners = []
        self.ops = ops
        self.l, self.r = ops
        for op in ops:
            if isinstance(op, Lazy):
                op.listeners.append(self)

    def recalc(self):
        pass

    def const(self):
        return ops[0].const and ops[1].const

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.ops[0])}, {repr(self.ops[1])})'

    
class Add(Op):
    @property
    def value(self):
        assert self.const
        return self.l + self.r

class Mul(Op):
    @property
    def value(self):
        assert self.const
        return self.l * self.r


class Div(Op):
    @property
    def value(self):
        assert self.const
        return self.l // self.r


class Mod(Op):
    @property
    def value(self):
        assert self.const
        return self.l % self.r


class Eq(Op):
    @property
    def value(self):
        assert self.const
        return int(self.l == self.r)


def monad2(a):
    state = dict((v, Const(0)) for v in 'xyzw')
    inps = []
    for l, (op, reg, *_arg) in enumerate(a):
        print(l, op, reg, _arg, state)
        if _arg:
            arg = _arg[0]
            argval = Const(arg) if isinstance(arg, int) else state[arg]
        else:
            arg = None
            argval = None
        regval = state[reg]
        if op == 'inp':
            inps.append(Var(len(inps)))
            state[reg] = inps[-1]
            s = str(state)
            print(inps, l, s)
            if len(s) > 1000:
                return None
        elif op == 'add':
            if arg == 0:
                pass
            elif regval.const and argval.const:
                state[reg] = regval.value + argval.value
            else:
                state[reg] = Add(regval, argval)
        elif op == 'mul':
            if arg == 0:
                state[reg] = 0
            elif arg == 1:
                pass
            elif regval.const and argval.const:
                state[reg] = regval.value * argval.value
            else:
                state[reg] = Mul(regval, argval)
        elif op == 'div':
            if arg == 1:
                pass
            elif regval.const and argval.const:
                state[reg] = regval.value // argval.value
            else:
                state[reg] = Div(regval, argval)
        elif op == 'mod':
            if arg == 1:
                state[reg] = 0
            elif regval.const and argval.const:
                state[reg] = regval.value % argval.value
            else:
                state[reg] = Mod(regval, argval)
        elif op == 'eql':
            if regval.const and argval.const:
                state[reg] = int(regval.value == argval.value)
            else:
                state[reg] = Eq(regval, argval)

    print("== ", state)

def first(a):
    f = monad2(a)
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
