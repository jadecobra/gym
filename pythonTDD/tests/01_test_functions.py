import unittest
import functions


class TestFunctions(unittest.TestCase):

    def test_functions_with_pass(self):
        self.assertIsNone(functions.function_with_pass())

    def test_functions_with_return(self):
        self.assertIsNone(functions.function_with_return())

    def test_functions_with_return_none(self):
        self.assertIsNone(functions.function_with_return_none())

    def test_passthrough(self):
        self.assertEqual(functions.passthrough(False), False)
        self.assertEqual(functions.passthrough(0), 0)
        self.assertEqual(functions.passthrough('my_first_name'), 'my_first_name')
        self.assertEqual(functions.passthrough(set((1, 2))) , {1, 2})
        self.assertEqual(
            functions.passthrough(
                list(('my_first_name', 'my_other_name'))
            ),
            ['my_first_name', 'my_other_name']
        )
        self.assertEqual(
            functions.passthrough(
                dict(my_first_name='my_first_name')
            ),
            {'my_first_name': 'my_first_name'}
        )
        self.assertEqual(functions.passthrough(tuple((4, 5))) , (4, 5))
        self.assertEqual(functions.passthrough(True) , True)

    def test_functions_with_unknown_number_of_parameters(self):
        self.assertEqual(functions.parameter_counter(1, 2, 3), 3)
        self.assertEqual(functions.parameter_counter(1, 2, 3, 4, 5), 5)

    def test_functions_with_positional_arguments(self):
        self.assertEqual(
            functions.passthrough_with_positions('my_first_name', 'my_last_name'),
            ('my_first_name', 'my_last_name')
        )
        self.assertEqual(
            functions.passthrough_with_positions('my_last_name', 'my_first_name'),
            ('my_first_name', 'my_last_name')
        )

    def test_functions_with_keyword_arguments(self):
        self.assertEqual(
            functions.passthrough_with_keywords(
                first_name='my_first_name', last_name='my_last_name'
            ),
            ('my_first_name', 'my_last_name')
        )
        self.assertEqual(
            functions.passthrough_with_keywords(
                last_name='my_last_name', first_name='my_first_name',
            ),
            ('my_first_name', 'my_last_name')
        )

    def test_functions_with_unknown_number_of_keyword_arguments(self):
        self.assertEqual(
            functions.keyword_counter(a=1, b=2, c=3, d=4), 4
        )
        self.assertEqual(
            functions.keyword_counter(a=1, b=2), 2
        )

    def test_functions_with_unknown_number_of_positional_arguments_and_keyword_arguments(self):
        self.assertEqual(
            functions.argument_counter(1, 2, 3, 4, a=5, b=6, c=7, d=8),
            8
        )
        self.assertEqual(
            functions.argument_counter(1, 2, c=7, d=8),
            4
        )

    def test_singleton_function(self):
        self.assertEqual(functions.name(), 'my_first_name')

    def test_singleton_function_with_input(self):
        self.assertEqual(functions.joe('Bob', 'James', 'Frank'), 'joe')

if __name__ == "__main__":
    unittest.main()