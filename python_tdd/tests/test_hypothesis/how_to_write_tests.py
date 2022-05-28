from hypothesis import given
from hypotehesis.strategies import (
    integers, lists, text, tuples, booleans
)

@given(integers(), integers())
def test_ints_are_commutative(x, y):
    assert x + y == y + x

@given(x=integers(), y=integers())
def test_ints_cancel(x, y):
    assert (x + y) - y == x

@given(lists(integers()))
def test_reversing_twice_gives_same_list(xs):
    # This will generate lists of arbitrary length
    # (usually between 0 and 100 elements) whose elements are integers
    ys = list(xs)
    ys.reverse()
    ys.reverse()
    assert xs == ys

@given(tuples(booleans(), text())
def test_look_tuples_work_too(t):
    # A tuple is generated as the one you provided,
    # with the corresponding types in those positions
    assert len(t) == 2
    assert isinstance(t[0], bool)
    assert isinstance(t[1], str)