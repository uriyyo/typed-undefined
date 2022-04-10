import pickle
from copy import copy, deepcopy
from typing import Union

from pytest import mark, raises

from undefined import Undefined, is_undefined, resolve, undefined


def test_singleton():
    assert Undefined() is Undefined()
    assert undefined is Undefined()


def test_subclass():
    with raises(RuntimeError, match="^Can't subclass Undefined$"):

        class _UndefinedSubclass(Undefined):
            pass


def test_is_false():
    assert not undefined


def test_repr_str():
    assert str(undefined) == "undefined"
    assert repr(undefined) == "Undefined()"


def test_copy_deepcopy_pickle():
    assert copy(undefined) is undefined
    assert deepcopy(undefined) is undefined
    assert pickle.loads(pickle.dumps(undefined)) is undefined


@mark.parametrize(
    "args,kwargs",
    (
        ((), {"a": 1}),
        ((1,), {}),
        ((1,), {"a": 1}),
    ),
    ids=[
        "kwargs",
        "args",
        "args-and-kwargs",
    ],
)
def test_singleton_args_kwargs(args, kwargs):
    with raises(TypeError, match="^Undefined does not accept args and kwargs$"):
        Undefined(*args, **kwargs)


def test_singleton_getitem():
    assert Undefined[int] == Union[Undefined, int]
    assert Undefined[int, float] == Union[Undefined, int, float]
    assert Undefined[Union[int, float]] == Union[Undefined, int, float]


@mark.parametrize(
    "value,default,expected",
    [
        (undefined, 1, 1),
        (1, 2, 1),
    ],
    ids=[
        "undefined",
        "non-undefined",
    ],
)
def test_resolve(value, default, expected):
    assert resolve(value, default) == expected


@mark.parametrize(
    "value,expected",
    [
        (undefined, True),
        (1, False),
    ],
    ids=[
        "undefined",
        "non-undefined",
    ],
)
def test_is_undefined(value, expected):
    assert is_undefined(value) == expected
