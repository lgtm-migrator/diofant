# Tests for var are in their own file, because var pollutes global namespace.

import pytest

from diofant import Function, FunctionClass, Symbol, symbols, var
from diofant.abc import a, b, d, e, x, y


bb, cc, zz, _x, fg = symbols('bb cc zz _x fg')

__all__ = ()

# make z1 with call-depth = 1


def _make_z1():
    var('z1')

# make z2 with call-depth = 2


def __make_z2():
    var('z2')


def _make_z2():
    __make_z2()


def test_var():
    var('a')
    assert a == Symbol('a')

    var('b bb cc zz _x')
    assert b == Symbol('b')
    assert bb == Symbol('bb')
    assert cc == Symbol('cc')
    assert zz == Symbol('zz')
    assert _x == Symbol('_x')

    v = var(['d', 'e', 'fg'])
    assert d == Symbol('d')
    assert e == Symbol('e')
    assert fg == Symbol('fg')

    # check return value
    assert v == [d, e, fg]

    # pylint: disable=undefined-variable

    # see if var() really injects into global namespace
    pytest.raises(NameError, lambda: z1)  # type: ignore[name-defined]
    _make_z1()
    assert z1 == Symbol('z1')

    pytest.raises(NameError, lambda: z2)  # type: ignore[name-defined]
    _make_z2()
    assert z2 == Symbol('z2')


def test_var_return():
    pytest.raises(ValueError, lambda: var(''))
    v2 = var('q')
    v3 = var('q p')

    assert v2 == Symbol('q')
    assert v3 == (Symbol('q'), Symbol('p'))


def test_var_accepts_comma():
    v1 = var('x y z')
    v2 = var('x,y,z')
    v3 = var('x,y z')

    assert v1 == v2
    assert v1 == v3


def test_var_keywords():
    var('x y', extended_real=True)
    assert x.is_extended_real and y.is_extended_real


def test_var_cls():
    f = var('f', cls=Function)

    assert isinstance(f, FunctionClass)

    g, h = var('g,h', cls=Function)

    assert isinstance(g, FunctionClass)
    assert isinstance(h, FunctionClass)


def test_var_nested():
    ((a, *_), (x, *_)) = var(('a:d', 'x:z'))
    assert isinstance(a, Symbol)
    assert isinstance(x, Symbol)
