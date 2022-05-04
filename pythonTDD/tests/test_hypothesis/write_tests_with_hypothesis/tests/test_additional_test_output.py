from hypothesis import given, note
from hypothesis.strategies import lists, integers, randoms
from unittest import TestCase

class TestAdditionTestOutput(TestCase):

    @given(lists(integers()), randoms())
    def test_shuffle_is_no_op(self, ls, r):
        ls2 = list(ls)
        r.shuffle(ls2)
        note(f"Shuffle: {ls2!r}")
        self.assertEqual(ls, ls2)

