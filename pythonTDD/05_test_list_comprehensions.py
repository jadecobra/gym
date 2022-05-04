import unittest
import list_comprehensions


class TestListComprehensions(unittest.TestCase):
    def test_creating_lists_from_a_collection(self):
        collection = range(10)
        a_list = []
        for element in collection:
            a_list.append(element)

        self.assertEqual(a_list, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(
            list(collection),
            a_list,
        )

    def test_creating_lists_with_a_for_loop(self):
        collection = range(10)
        a_list = []
        for element in collection:
            a_list.append(element)

        self.assertEqual(a_list, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(
            list_comprehensions.for_loops(collection),
            a_list,
        )

    def test_creating_lists_with_a_list_comprehension(self):
        collection = range(10)
        a_list = []
        for element in collection:
            a_list.append(element)

        self.assertEqual(a_list, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(
            [element for element in collection],
            a_list,
        )

    def test_list_comprehensions_with_conditions(self):
        collection = range(10)
        even_numbers = []
        for element in collection:
            if element % 2 == 0:
                even_numbers.append(element)

        self.assertEqual(even_numbers, [0, 2, 4, 6, 8])
        self.assertEqual(
            [element for element in collection if element % 2 == 0],
            a_list,
        )

    def test_list_comprehensions_with_and_conditions(self):
        collection = range(10)
        result = []
        for element in collection:
            if element % 2 == 0 and element % 3 == 0:
                result.append(element)

        self.assertEqual(result, [0, 6])
        self.assertEqual(
            [
                element
                for element in collection
                if element % 2 == 0 and element % 3 == 0
            ],
            result,
        )

    def test_list_comprehensions_with_or_conditions(self):
        collection = range(10)
        result = []
        for element in collection:
            if element % 2 == 0 or element % 3 == 0:
                result.append(element)

        self.assertEqual(result, [0, 2, 4, 6, 8, 3, 9])
        self.assertEqual(
            [
                element
                for element in collection
                if element % 2 == 0 and element % 3 == 0
            ],
            result,
        )
