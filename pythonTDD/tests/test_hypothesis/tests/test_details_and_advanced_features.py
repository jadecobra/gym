import unittest
import hypothesis
import math


class TestDetailsAndAdvancedFeatures(unittest.TestCase):

    @hypothesis.given(hypothesis.strategies.lists(hypothesis.strategies.integers()), hypothesis.strategies.randoms())
    def test_reporting_values_for_minimal_failing_example(self, ls, r):
        ls2 = list(ls)
        r.shuffle(ls2)
        hypothesis.note(f'Shuffle: {ls2!r}')
        try:
            self.assertEqual(ls, ls2)
        except AssertionError:
            'ls != ls2'

    @hypothesis.given(hypothesis.strategies.integers().filter(lambda x: x % 2 == 0))
    def test_record_an_event(self, integer):
        hypothesis.event(f"integer mod 3 = {integer % 3}")

    @hypothesis.given(hypothesis.strategies.floats())
    def test_making_assumptions(self, x):
        hypothesis.assume(not math.isnan(x))
        self.assertEqual(x, -(-x))