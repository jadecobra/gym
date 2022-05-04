from unittest import TestCase
from hypothesis import given
from hypothesis.strategies import (
    integers, lists, text, tuples, booleans
)

class TestWritingTests(TestCase):

    @given(integers(), integers())
    def test_ints_are_commutative(self, x, y):
        self.assertEqual(x + y, y + x)

    @given(x=integers(), y=integers())
    def test_ints_cancel(self, x, y):
        self.assertEqual((x + y) - y, x)

    @given(lists(integers()))
    def test_reversing_twice_gives_same_list(self, xs):
        # This will generate lists of arbitrary length
        # (usually between 0 and 100 elements) whose elements are integers
        ys = list(xs)
        ys.reverse()
        ys.reverse()
        self.assertEqual(xs, ys)

    @given(tuples(booleans(), text()))
    def test_look_tuples_work_too(self, t):
        # A tuple is generated as the one you provided,
        # with the corresponding types in those positions
        self.assertEqual(len(t), 2)
        self.assertIsInstance(t[0], bool)
        self.assertIsInstance(t[1], str)
