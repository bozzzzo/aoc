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




class Lazy(object):
    @property
    def zero(self):
        return self.const and self.value == 0

    @property
    def one(self):
        return self.const and self.value == 1

    pass

class Const(Lazy):
    def __init__(self, value):
        self.value = value

    @property
    def const(self):
        return True

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    @property
    def vars(self):
        return set()

    def bind(self, ctx):
        return self.value

    @property
    def values(self):
        return {self.value}

    @property
    def positive(self):
        return self.value > 0

    def rebind(self, ctx):
        return self

class Var(Lazy):
    NAMES = iter('abcdefghijklmnop')

    @classmethod
    def reset_names(cls):
        cls.NAMES = iter('abcdefghijklmnop')


    def __init__(self, i, value=frozenset(range(1,10)), name=None):
        self.name = next(self.NAMES) if name is None else name
        self.i = i
        self._value = value

    @property
    def value(self):
        assert self.const
        return self._value if isinstance(self._value, int) else tuple(self._value)[0]

    @property
    def const(self):
        return isinstance(self._value, int) or len(self._value) == 1

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}{tuple(sorted(self.values))}"

    @property
    def vars(self):
        return set([self])

    def bind(self, ctx):
        assert self in ctx
        assert ctx[self] in self._value
        return ctx[self]

    @property
    def values(self):
        return self._value

    @property
    def positive(self):
        return min(self.values) > 0

    def rebind(self, ctx):
        return ctx.get(self, self)


class Op(Lazy):
    def __init__(self, *ops):
        self.ops = ops
        self.l, self.r = ops
        assert isinstance(self.l, Lazy), f"?? {type(self.l)} {self.l}"
        assert isinstance(self.r, Lazy), f"?? {type(self.r)} {self.r}"
        self._possibilities = None

    @property
    def const(self):
        return self.l.const and self.r.const

    def __str__(self):
        return f'({str(self.l)} {self.REP} {str(self.r)})'

    def __repr__(self):
        return f'({repr(self.l)} {self.REP} {repr(self.r)})'

    @property
    def value(self):
        assert self.const
        return int(self.OP(self.l.value, self.r.value))

    @property
    def vars(self):
        return self.l.vars | self.r.vars

    def bind(self, ctx):
        return int(self.OP(self.l.bind(ctx), self.r.bind(ctx)))

    @property
    def values(self):
        return set(int(self.OP(l,r)) for l,r in itertools.product(self.l.values, self.r.values))

    def rebind(self, ctx):
        return type(self)(self.l.rebind(ctx), self.r.rebind(ctx))


class Add(Op):
    OP = operator.add
    REP = '+'

    @property
    def positive(self):
        return self.l.positive and self.r.positive


class Mul(Op):
    OP = operator.mul
    REP = '*'

    @property
    def positive(self):
        return self.l.positive == self.r.positive

class Div(Op):
    OP = operator.floordiv
    REP = '/'

    @property
    def positive(self):
        return False


class Mod(Op):
    OP = operator.mod
    REP = '%'

class Eq(Op):
    OP = lambda s,x,y: int(x==y)
    REP = '=='

def show(state):
    return ", ".join(f"{n}={v}" for n,v in state.items())

def fork(*, state, inps, history, reg, l):
    expr = state[reg]
    used = expr.vars
    if not used:
        assert expr.const
        return [(state, inps, history)]
    used_names = {var.name for var in used}
    unused = {var for var in inps if var.name not in used_names}
    unused_names = {var.name for var in unused}
    inp_names = {var.name for var in inps}
    assert len(used_names) == len(used)
    assert len(unused_names) == len(unused)
    assert len(inp_names) == len(inps)
    assert len(used_names|unused_names) == len(inp_names)
    assert not (used_names & unused_names), f"{used_names} intersects {unused_names}, inps={inps}"
    assert inp_names == (used_names | unused_names)
    new = collections.defaultdict(lambda: {v: Var(v.i, set(), name=v.name) for v in used})
    for ctx in map(dict, itertools.product(*[[(var, val) for val in var.values] for var in used])):
        res = expr.bind(ctx)
        for var, val in ctx.items():
            new[res][var].values.add(val)
    new_states = []
    for res, used_map in new.items():
        new_state = {k:v.rebind(used_map) for k,v in state.items()}
        new_state[reg] = Const(res)
        new_inps = unused | set(used_map.values())
        new_history = history + ((l, res),)
        print(f"              #  new_state {reg}={new_state[reg]} inps {repr(new_inps)} history {new_history}")
        new_states.append((new_state, new_inps, new_history))
    return new_states


def monad2(a, values=None, **kwargs):
    if values is None:
        values = [set(range(1,10))] * 14
    state_ = dict((v, kwargs.get(v, Const(0))) for v in 'xyzw')
    states = [(state_, set(), ())]
    _26 = Const(26)
    assert _26 == Const(26)
    zero = Const(0)
    one = Const(1)
    Var.reset_names()
    for l, (op, reg, *_arg) in enumerate(a):
        new_states = []
        if op == 'inp':
            print()
        for state, inps, history in states:
            regval = state[reg]
            if _arg:
                arg = _arg[0]
                argval = Const(arg) if isinstance(arg, int) else state[arg]
            else:
                arg = None
                argval = None
            if op == 'inp':
                state[reg] = Var(len(inps), value=values[len(inps)], name=f"{reg}{len(inps)+1}")
                inps.add(state[reg])
            elif op == 'add':
                if regval.zero:
                    state[reg] = argval
                elif argval.zero:
                    pass
                elif regval.const and isinstance(argval, Add) and argval.l.const:
                    state[reg] = Add(Const(regval.value + argval.l.value), argval.r)
                elif regval.const and isinstance(argval, Add) and argval.r.const:
                    state[reg] = Add(argval.l, Const(regval.value + argval.r.value))
                elif argval.const and isinstance(regval, Add) and regval.l.const:
                    state[reg] = Add(Const(argval.value + regval.l.value), regval.r)
                elif argval.const and isinstance(regval, Add) and regval.r.const:
                    state[reg] = Add(regval.l, Const(argval.value + regval.r.value))
                else:
                    state[reg] = Add(regval, argval)
            elif op == 'mul':
                if regval.zero or argval.zero:
                    state[reg] = zero
                elif regval.one:
                    state[reg] = argval
                elif argval.one:
                    pass
                elif regval.const and isinstance(argval, Mul) and argval.l.const:
                    state[reg] = Mul(Const(regval.value + argval.l.value), argval.r)
                elif regval.const and isinstance(argval, Mul) and argval.r.const:
                    state[reg] = Mul(argval.l, Const(regval.value + argval.r.value))
                elif argval.const and isinstance(regval, Mul) and regval.l.const:
                    state[reg] = Mul(Const(argval.value + regval.l.value), regval.r)
                elif argval.const and isinstance(regval, Mul) and regval.r.const:
                    state[reg] = Mul(regval.l, Const(argval.value + regval.r.value))
                else:
                    state[reg] = Mul(regval, argval)
            elif op == 'div':
                if argval.one:
                    pass
                elif isinstance(regval, Add) and isinstance(regval.l, Mul) and regval.l.r == argval:
                    state[reg] = regval.l.l
                elif isinstance(regval, Add) and isinstance(regval.r, Mul) and regval.r.r == argval:
                    state[reg] = regval.r.l
                else:
                    state[reg] = Div(regval, argval)
            elif op == 'mod':
                if isinstance(regval, Add) and isinstance(regval.l, Mul) and regval.l.r == argval:
                    state[reg] = regval.r
                elif isinstance(regval, Add) and isinstance(regval.r, Mul) and regval.r.r == argval:
                    state[reg] = regval.l
                else:
                    mod = Mod(regval, argval)
                    if mod.values != regval.values:
                        state[reg] = mod
            elif op == 'eql':
                state[reg] = Eq(regval, argval)

            else:
                assert False, f"Unknown '{op} {reg} {_arg}'"

            print(f'{l:3} {op:3} {reg} {("" if arg is None else arg):3} #   {reg}={state[reg]}', end='')

            # constant folding
            if state[reg].const and not isinstance(state[reg], Const):
                const = Const(state[reg].value)
                print(f"  => {const}")
                state[reg] = const
            else:
                print()

            if isinstance(state[reg], Eq):
                new_states.extend(fork(state=state,inps=inps,history=history,reg=reg,l=l))

        if new_states:
            states = new_states


    def solutions():
        for pstate, pinps, phistory in states:
            pz = pstate['z']
            if pz.positive:
                print(f'no possible solution for {pz}')
                continue
            print(f'evaluating {pz}')
            for state, inps, history in fork(state=pstate, inps=pinps, history=phistory, reg='z', l='z'):
                z = state['z']
                if z.value == 0:
                    inps = sorted(inps, key=lambda v:v.i)
                    print(f'found zero solution for {pz} with {inps} history {history}')
                    yield inps
                    break
            else:
                print(f'no zero solution for {pz}')

    # print("== ", state)
    return list(solutions())







def first(a):



    z = monad2(a)
    assert len(z) == 1
    soln, = z
    biggest = [(max(var.values)) for var in soln]
    smallest = [(min(var.values)) for var in soln]

    proof = monad2(a, values=[{v} for v in biggest])
    assert proof

    return "".join(map(str, biggest)), "".join(map(str, smallest))
    pass

def second(a):
    pass


def test():
    def _(a,b):
        print()
        assert a==b, f"{a}!={b}"

    a = Const(10)
    b = Var(0, name='test_b')
    assert str(b) == 'test_b'
    assert repr(b) == 'test_b(1, 2, 3, 4, 5, 6, 7, 8, 9)', repr(b)
    eq = Eq(a,b)
    assert not eq.const, eq
    assert str(eq) == '(10 == test_b)'

    eq2 = Eq(eq,a)
    assert not eq2.const, eq2
    print(eq2)
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
    return tuple(map(parse_insn, filter(str.strip, (l.split('#')[0] for l in f.splitlines()))))
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
