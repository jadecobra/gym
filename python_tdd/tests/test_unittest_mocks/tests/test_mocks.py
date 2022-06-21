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
        args = (1, 2)
        kwargs =  {'keyA':'valueA', 'keyN':'valueN'}

        mocked_object = unittest.mock.Mock()
        mocked_object.method(*args, **kwargs)
        mocked_object.method.assert_called_with(*args, **kwargs)

    def test_assert_called_exactly_once(self):
        args = ('a', 'b')
        kwargs = dict(keyC='valueC', keyN='valueN')

        mocked_object = unittest.mock.Mock(return_value=None)
        mocked_object(*args, **kwargs)
        mocked_object.assert_called_once_with(*args, **kwargs)

        mocked_object('other', bar='values')
        with self.assertRaises(AssertionError):
            mocked_object.assert_called_once_with('other', bar='values')

    def test_assert_any_call(self):
        args = ('a', 'b')
        kwargs = dict(keyC='valueC', keyN='valueN')

        mocked_object = unittest.mock.Mock(return_value=None)
        mocked_object(*args, **kwargs)
        mocked_object('some', 'thing', 'else')
        mocked_object.assert_any_call(*args, **kwargs)

    def test_assert_has_calls(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        self.assertIsNone(mocked_object(1))
        self.assertIsNone(mocked_object(2))
        self.assertIsNone(mocked_object(3))
        self.assertIsNone(mocked_object(4))

        mocked_object.assert_has_calls(
            [unittest.mock.call(2), unittest.mock.call(3)]
        )

        with self.assertRaises(AssertionError):
            mocked_object.assert_has_calls(
                [unittest.mock.call(4), unittest.mock.call(2), unittest.mock.call(3)],
                any_order=False
            )

        mocked_object.assert_has_calls(
            [unittest.mock.call(4), unittest.mock.call(2), unittest.mock.call(3)],
            any_order=True
        )

    def test_assert_not_called(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.hello.assert_not_called()
        mocked_object.hello()
        with self.assertRaises(AssertionError):
            mocked_object.hello.assert_not_called()

    def test_resetting_all_the_call_attributes_on_a_mock(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        mocked_object('hello')
        self.assertTrue(mocked_object.called)
        mocked_object.reset_mock()
        self.assertFalse(mocked_object.called)

    def test_setting_attributes_on_mock_through_keyword_arguments(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.configure_mock(
            **{
                'method.return_value': 3,
                'raises_error.side_effect': KeyError
            }
        )
        self.assertEqual(mocked_object.method(), 3)
        with self.assertRaises(KeyError):
            mocked_object.raises_error()

    def test_setting_attributes_during_mock_construction(self):
        mocked_object = unittest.mock.Mock(
            attribute_a='eggs',
            **{
                'method.return_value': 3,
                'raises_error.side_effect': ValueError
            }
        )
        self.assertEqual(mocked_object.attribute_a, 'eggs')
        self.assertEqual(mocked_object.method(), 3)
        with self.assertRaises(ValueError):
            mocked_object.raises_error()

    def test_asserting_mock_calls(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        self.assertFalse(mocked_object.called)

        mocked_object()
        self.assertTrue(mocked_object.called)

    def test_counting_calls(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        self.assertEqual(mocked_object.call_count, 0)

        mocked_object()
        mocked_object()
        self.assertEqual(mocked_object.call_count, 2)

    def test_configuring_value_returned_by_calling_monk(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.Mock()
        mocked_object.return_value = return_value
        self.assertEqual(mocked_object(), return_value)

    def test_default_return_value(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.return_value.attribute = sentinel.Attribute
        mocked_object.return_value()
