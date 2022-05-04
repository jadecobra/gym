import unittest
import list_comprehensions


class TestListComprehensions(unittest.TestCase):

    def test_list_comprehensions(self):
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0],
            [0, 2, 4, 6, 8]
        )
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0 and x % 3 == 0],
            [0, 6]
        )
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0 or x % 3 == 0],
            [0, 2, 4, 6, 8, 3, 9]
        )
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0 and x % 3 == 0 or x % 5 == 0],
            [0, 6, 5]
        )
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0 and x % 3 == 0 or x % 5 == 0 and x % 7 == 0],
            [0, 6, 5, 7]
        )
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0 and x % 3 == 0 or x % 5 == 0 and x % 7 == 0 and x % 11 == 0],
            [0, 6, 5, 7, 11]
        )
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0 and x % 3 == 0 or x % 5 == 0 and x % 7 == 0 and x % 11 == 0 and x % 13 == 0],
            [0, 6, 5, 7, 11, 13]
        )
        self.assertEqual(
            [x for x in range(10) if x % 2 == 0 and x % 3 == 0 or x % 5 == 0 and x % 7 == 0 and x % 11 == 0 and x % 13 == 0 and x % 17 == 0],
            [0, 6, 5, 7, 11, 13, 17]
        )
        self.assertEqual(
            [x for x in range(10) if x