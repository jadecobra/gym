import unittest
import unittest.mock
import module

from utilities import POSITIONAL_ARGUMENTS, KEYWORD_ARGUMENTS


class TestSideEffect(unittest.TestCase):

    def test_returning_a_callable_with_side_effect(self):
        mocked_object = unittest.mock.Mock(
            side_effect=module.function(),
            return_value=None,
        )
        self.assertIsInstance(mocked_object, unittest.mock.Mock)

        for key in module.function():
            with self.subTest(i=key):
                self.assertEqual(mocked_object(), key)
        with self.assertRaises(StopIteration):
            mocked_object()

    def test_side_effect_with_dictionaries(self):
        def method(arg):
            return KEYWORD_ARGUMENTS[arg]

        mocked_object = unittest.mock.Mock()
        mocked_object.side_effect = method

        for key, value in KEYWORD_ARGUMENTS.items():
            with self.subTest(i=key):
                self.assertEqual(mocked_object(key), value)
        with self.assertRaises(KeyError):
            mocked_object('non-existent-key')

    def test_side_effects_with_iterables(self):
        def a_list():
            return [1, 2, 3, 'N']

        def a_tuple():
            return (1, 2, 3, 'N')

        mocked_object = unittest.mock.Mock()
        mocked_object.side_effect = a_list()

        for item in a_list():
            with self.subTest(i=item):
                self.assertEqual(mocked_object(), item)
        with self.assertRaises(StopIteration):
            mocked_object()

        mocked_object.side_effect = a_tuple()

        for item in a_tuple():
            with self.subTest(i=item):
                self.assertEqual(mocked_object(), item)
        with self.assertRaises(StopIteration):
            mocked_object()

    def test_exception_handling_with_side_effects(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.side_effect = Exception('BOOM!')
        with self.assertRaises(Exception):
            mocked_object()

    def test_setting_exceptions_in_constructor(self):
        mocked_object = unittest.mock.Mock(
            side_effect=Exception('BOOM!'),
            return_value=None,
        )
        self.assertIsInstance(mocked_object, unittest.mock.Mock)
        with self.assertRaises(Exception):
            mocked_object()

    def test_index_error_side_effect(self):
        mocked_object = unittest.mock.MagicMock(side_effect=IndexError)
        with self.assertRaises(IndexError):
            mocked_object(*POSITIONAL_ARGUMENTS)

        self.assertEqual(
            mocked_object.mock_calls,
            [unittest.mock.call(*POSITIONAL_ARGUMENTS)]
        )

    def test_setting_side_effects_in_constructor(self):
        mocked_object = unittest.mock.Mock(side_effect=lambda value: value + 1)
        self.assertEqual(mocked_object(-1), 0)
        self.assertEqual(mocked_object(0), 1)
        self.assertEqual(mocked_object(1), 2)

    def test_clearing_side_effect(self):
        mocked_object = unittest.mock.Mock(side_effect=Exception, return_value=3)
        with self.assertRaises(Exception):
            mocked_object()

        mocked_object.side_effect = None
        self.assertEqual(mocked_object(), 3)