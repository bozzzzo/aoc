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

class Context:
    def __init__(self, *args):
        self.data = dict(*args)
        self._encoding = None

    def merge(self, other):
        common = set(self.data).intersection(other.data)
        if all(self.data[v] == other.data[v] for v in common):
            return Context(itertools.chain(self.data.items(), other.data.items()))
        else:
            return None

    def __lt__(self, other):
        return self.encode() < other.encode()

    def encode(self):
        if self._encoding is None:
            self.encoding = tuple(
                v for i,v in sorted((k.i, v)
                                    for k,v in self.data.items()))
        return self._encoding

class Lazy:
    pass

class Const:
    def __init__(self, value):
        self.value = value

    @property
    def const(self):
        return True

    def possibilities(self):
        return {self.value: Context()}

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    vars = set()

class Var(Lazy):
    NAMES = iter('abcdefghijklmnop')
    _VARS = {}

    @classmethod
    def getVar(cls, name):
        return cls._VARS[name]

    @classmethod
    def reset_names(cls):
        cls.NAMES = iter('abcdefghijklmnop')


    def __init__(self, i, value=range(1,10)):
        self.name = next(self.NAMES)
        self._VARS[self.name] = self
        self.listeners = []
        self.i = i
        self._value = value
        self.vars = set(self.name)

    @property
    def value(self):
        assert self.const
        return self._value

    @property
    def const(self):
        return isinstance(self._value, int)

    def possibilities(self):
        if isinstance(self._value, int):
            vals = (self._value, )
        else:
            vals = self._value

        return {val:Context(((self, val),)) for val in vals}

    def set(self, value):
        self.value = value
        for l in listeners:
            l.recalc()

    def __repr__(self):
        op = self.__class__.__name__
        if self.const:
            op = op +'!'
        return f"{self.name}"


class Op(Lazy):
    def __init__(self, *ops):
        self.listeners = []
        self.ops = ops
        self.l, self.r = ops
        self._possibilities = None
        self.vars = self.l.vars | self.r.vars
        for op in ops:
            if isinstance(op, Lazy):
                op.listeners.append(self)

    def recalc(self):
        self._possibilities = None
        for parent in self.listeners:
            parent.recalc()
        pass

    @property
    def const(self):
        return self.l.const and self.r.const

    def __repr__(self):
        op = self.__class__.__name__
        p = self.possibilities()
        ps = ",".join(map(str,p[:3]))
        if len(p) > 3:
            ps += f'...{len(p)}'
        return f'{self.REP}[{ps}]'

    @property
    def value(self):
        assert self.const
        return Const(int(self.OP(self.l.value, self.r.value)))

    def possibilities(self):
        p = self._possibilities
        if p is None:
            self._possibilites = p = {}
            for (l, lv), (r, rv) in itertools.product(self.l.possibilities().items(), self.r.possibilities().items()):
                c = lv.merge(rv)
                if c is None:
                    continue
                val = self.OP(l,r)
                if val not in p:
                    p[val] = c
                else:
                    p[val] = better_of(p[val], c)
        return p


class Add(Op):
    OP = operator.add
    REP = '+'

class Mul(Op):
    OP = operator.mul
    REP = '*'

class Div(Op):
    OP = operator.floordiv
    REP = '/'

class Mod(Op):
    OP = operator.mod
    REP = '%'

class Eq(Op):
    OP = operator.eq
    REP = '=='


def monad2(a):
    state = dict((v, Const(0)) for v in 'xyzw')
    inps = []
    Var.reset_names()
    for l, (op, reg, *_arg) in enumerate(a):
        if _arg:
            arg = _arg[0]
            argval = Const(arg) if isinstance(arg, int) else state[arg]
        else:
            arg = None
            argval = None
        regval = state[reg]
        if op == 'inp':
            print()
            inps.append(Var(len(inps)))
            state[reg] = inps[-1]
        elif op == 'add':
            state[reg] = Add(regval, argval)
        elif op == 'mul':
            state[reg] = Mul(regval, argval)
        elif op == 'div':
            state[reg] = Div(regval, argval)
        elif op == 'mod':
            state[reg] = Mod(regval, argval)
        elif op == 'eql':
            state[reg] = Eq(regval, argval)
        else:
            assert False
        s = str(state)
        print(l, op, reg, _arg, s)
        if len(s) > 1000:
            return None


    print("== ", state)

def first(a):
    global better_of
    def better_of(c1,c2):
        return c2 if c2 > c1 else c1

    f = monad2(a)
    pass

def second(a):
    pass


def test():
    def _(a,b):
        print()
        assert a==b, f"{a}!={b}"

    assert not Var(1).const
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
