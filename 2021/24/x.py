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
from typing import *
from pprint import pprint
import sys


def fst(x):
    return x[0]

def snd(x):
    return x[1]

dbg = False

def irange(a,b):
    d = 1 if b >= a else -1
    return range(a,b+d,d)

def srange(a,b):
    return irange(a,b) if a < b else irange(b,a)


class Context:
    def __init__(self, data):
        self.data = data
        self._encoding = None

    def __repr__(self):
        p = ", ".join(map(str, self.data[:2]))
        return f"{p}...[{len(self.data)}]"

    def merge(self, other):
        dbg and print("merge >>", self, other)
        def inner():
            for ds, do in itertools.product(self.data, other.data):
                ks = set(ds)
                ko = set(do)
                kc = ks.intersection(ko)
                if not all(ds[k] == do[k] for k in kc):
                    dbg and print(f"merge no solution for {ds} {do} due to {kc}")
                    continue
                yield dict(itertools.chain(ds.items(), do.items()))
        possibilities = tuple(inner())
        dbg and print("merge << ", possibilities)
        if not possibilities:
            return None
        return Context(possibilities)

    def combine(self, other):
        dbg and print("combine >>", self, other)
        ret = Context(self.data + other.data)
        dbg and print("combine <<", ret)
        return ret

    def __lt__(self, other):
        return self.encode() < other.encode()

    def encode(self):
        if self._encoding is None:
            self._encoding = tuple(
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
        return {self.value: Context(({},))}

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value


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

        return {val: Context(({self: val},)) for val in vals}

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
        ps = ", ".join(map(str, itertools.islice(p.items(),3)))
        return f'{self.REP}[{ps}....{len(p)}]'

    @property
    def value(self):
        assert self.const
        return Const(int(self.OP(self.l.value, self.r.value)))

    def possibilities(self):
        p = self._possibilities
        if p is None:
            self._possibilites = p = {}
            for (l, lv), (r, rv) in itertools.product(self.l.possibilities().items(), self.r.possibilities().items()):
                val = self.OP(l,r)
                dbg and print(f'merge of       {val}={l}{self.REP}{r} lv:{lv} rv:{rv}')
                c = lv.merge(rv)
                if c is None:
                    dbg and print(f'merge conflict {val}={l}{self.REP}{r} lv:{lv} rv:{rv}')
                    continue
                if val not in p:
                    dbg and print(f'merge first    {val}={l}{self.REP}{r} lv:{lv} rv:{rv} c:{c}')
                    p[val] = c
                else:
                    np = p[val].combine(c)
                    dbg and print(f'merge existing {val}={l}{self.REP}{r} lv:{lv} rv:{rv} c:{c} pval:{p[val]} np:{np}')
                    p[val] = np
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
    OP = lambda s,x,y: int(x==y)
    REP = '=='


def monad2(a, **kwargs):
    state = dict((v, kwargs.get(v, Const(0))) for v in 'xyzw')
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
            if arg == 0:
                state[reg] = Const(0)
            else:
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
        if len(s) > 10000:
            return None


    print("== ", state)
    return state['z'].possibilities()

def first(a):

    def chop(a):
        part = []
        for insn in a:
            op, *_ = insn
            if op == 'inp' and part:
                yield part
                part = []
            part.append(insn)
        yield part

    parts = list(chop(a))
    print(parts)

    f = monad2(parts[-1], z=Var(13,range(-100,100)))
    print("=====", f)

    # f = monad2(a)

    return f[0]
    pass

def second(a):
    pass


def test():
    def _(a,b):
        print()
        assert a==b, f"{a}!={b}"

    a = Var(0, (1,2))
    print("a=", a, a.possibilities())
    aea = Eq(a,a)
    print("a==a=", aea)
    b = Var(1, (1,2,3))
    print("b=", b, b.possibilities())
    atb = Mul(a,b)
    print("a*b=", atb)
    apb = Add(a, b)
    print("a+b=", apb)
    m = Mod(atb, apb)
    print("%=", m)

    
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
             ("input")][1:2
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
