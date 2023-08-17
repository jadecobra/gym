from unittest import TestCase
from random import randint

import iterations
import itertools
import operator

class TestInfiniteIterators(TestCase):

    def test_accumulate(self):
        self.assertEqual(
            list(iterations.accumulate_results_of_binary_functions([1, 2, 3, 4, 5])),
            list(itertools.accumulate([1, 2, 3, 4, 5]))
        )

    def data(self):
        return [3, 4, 6, 2, 1, 9, 0, 7, 5, 8]

    def test_running_product(self):
        self.assertEqual(
            list(itertools.accumulate(self.data(), operator.mul)),
            [3, 12, 72, 144, 144, 1296, 0, 0, 0, 0]
        )

    def test_running_maximum(self):
        self.assertEqual(
            list(itertools.accumulate(self.data(), max)),
            [3, 4, 6, 6, 6, 9, 9, 9, 9, 9]
        )

    def test_running_minimum(self):
        self.assertEqual(
            list(itertools.accumulate(self.data(), min)),
            [3,3,3,2,1,1,0,0,0,0]
        )

    def test_amortization(self):
        def future_value(balance, payment, interest=.05):
            return (balance * (1 + interest)) + payment
        cash_flows = [1000, -90, -90, -90, -90]
        self.assertEqual(
            list(
                itertools.accumulate(cash_flows, future_value)),
            [1000, 960.0, 918.0, 873.9000000000001, 827.5950000000001]
        )

    def test_chaotic_recurrence_relation(self):
        def logistic_map(x, _, r=3.8):
            return r * x * (1 - x)

        self.assertEqual(
            [f'{x:.2f}' for x in itertools.accumulate(itertools.repeat(0.4, 16), logistic_map)],
            [
                '0.40', '0.91', '0.30', '0.81',
                '0.60', '0.92', '0.29', '0.79',
                '0.63', '0.88', '0.39', '0.90',
                '0.33', '0.84', '0.52', '0.95'
            ]
        )

    def test_chain(self):
        self.assertEqual(
            list(iterations.chain('ABC', 'DEF')),
            list(itertools.chain('ABC', 'DEF'))
        )
        self.assertEqual(
            list(itertools.chain('ABC', 'DEF')),
            ['A', 'B', 'C', 'D', 'E', 'F']
        )

    def test_compress(self):
        self.assertEqual(
            list(iterations.compress('ABCDEF', [1, 0, 1, 0, 1, 1])),
            list(itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1]))
        )
        self.assertEqual(
            list(itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1])),
            ['A', 'C', 'E', 'F']
        )

    def test_dropwhile(self):
        def less_than_five(value):
            return value < 5
        self.assertEqual(
            list(iterations.drop_while_predicate_true(less_than_five, [1, 4, 6, 4, 1])),
            list(itertools.dropwhile(less_than_five, [1, 4, 6, 4, 1]))
        )
        self.assertEqual(
            list(itertools.dropwhile(less_than_five, [1, 4, 6, 4, 1])),
            [6, 4, 1]
        )


    def test_filterfalse(self):
        def is_even(value):
            return value % 2
        self.assertEqual(
            list(iterations.filter_false(is_even, range(10))),
            list(itertools.filterfalse(is_even, range(10)))
        )
        self.assertEqual(
            list(itertools.filterfalse(is_even, range(10))),
            [0, 2 ,4, 6, 8]
        )

    def test_groupby(self):
        self.assertEqual(
            [key for key, group in iterations.groupby('AAAABBBCCD')],
            [key for key, group in itertools.groupby('AAAABBBCCD')]
        )
        self.assertEqual(
            [list(group) for key, group in iterations.groupby('AAAABBBCCD')],
            [list(group) for key, group in itertools.groupby('AAAABBBCCD')],
        )

    def test_islice(self):
        pass

    def test_pairwise(self):
        pass

    def test_starmap(self):
        pass

    def test_takewhile(self):
        pass

    def test_tee(self):
        pass

    def test_zip_longest(self):
        pass
