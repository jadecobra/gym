import unittest
import unittest.mock
import module


class TestMocks(unittest.TestCase):

    def test_sending_exceptions(self):
        mocked_object = unittest.mock.Mock(
            side_effect=Exception,
            return_value=None,
        )
        self.assertIsInstance(mocked_object, unittest.mock.Mock)
        with self.assertRaises(Exception):
            mocked_object()

    def test_side_effects(self):
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

    def test_assigning_custom_side_effects(self):
        def values():
            return {'a': 1, 'b': 2, 'c': 3, 'n': 'N'}

        def method(arg):
            return values()[arg]

        mocked_object = unittest.mock.Mock()
        mocked_object.side_effect = method

        for key, value in values().items():
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

    def test_patching_magic_methods_with_mock_class(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.Mock()
        mocked_object.__str__ = unittest.mock.Mock(return_value=return_value)

        self.assertEqual(str(mocked_object), return_value)

    def test_assert_mock_called_at_least_once(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.method()
        mocked_object.method.assert_called()

    def test_assert_mock_called_only_once(self):
        mocked_object = unittest.mock.Mock()

        mocked_object.method()
        mocked_object.method.assert_called_once()

        mocked_object.method()
        with self.assertRaises(AssertionError):
            mocked_object.method.assert_called_once()

    def test_assert_called_with(self):
        mocked_object = unittest.mock.Mock()

        args = (1, 2, 3, {'test':'boom'})
        mocked_object.method(*args)
        mocked_object.method.assert_called_with(*args)

    def test_assert_called_once_with(self):
        args = ('a', 'b')
        kwargs = dict(keyC='valueC', keyN='valueN')
        mocked_object = unittest.mock.Mock(return_value=None)
        mocked_object(*args, **kwargs)
        mocked_object.assert_called_once_with(*args)
