import unittest
import unittest.mock
import module

from utilities import POSITIONAL_ARGUMENTS, KEYWORD_ARGUMENTS


class TestMocks(unittest.TestCase):

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
        mocked_object.method(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        mocked_object.method.assert_called_with(
            *POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS
        )

    def test_assert_called_exactly_once(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        mocked_object(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        mocked_object.assert_called_once_with(
            *POSITIONAL_ARGUMENTS,
            **KEYWORD_ARGUMENTS
        )

        mocked_object('other', bar='values')
        with self.assertRaises(AssertionError):
            mocked_object.assert_called_once_with('other', bar='values')

    def test_assert_any_call(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        mocked_object(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        mocked_object('some', 'thing', 'else')
        mocked_object.assert_any_call(
            *POSITIONAL_ARGUMENTS,
            **KEYWORD_ARGUMENTS
        )

    def test_assert_has_calls(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        self.assertIsNone(mocked_object(1))
        self.assertIsNone(mocked_object(2))
        self.assertIsNone(mocked_object(3))
        self.assertIsNone(mocked_object(4))

        mocked_object.assert_has_calls(
            [
                unittest.mock.call(2),
                unittest.mock.call(3)
            ]
        )

        with self.assertRaises(AssertionError):
            mocked_object.assert_has_calls(
                [
                    unittest.mock.call(4),
                    unittest.mock.call(2),
                    unittest.mock.call(3)
                ],
                any_order=False
            )

        mocked_object.assert_has_calls(
            [
                unittest.mock.call(4),
                unittest.mock.call(2),
                unittest.mock.call(3)
            ],
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

    def test_configuring_value_returned_by_calling_mock(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.Mock()
        mocked_object.return_value = return_value
        self.assertEqual(mocked_object(), return_value)

    def test_return_value(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.return_value.attribute = module.ClassC.attribute

        self.assertIsNone(module.ClassC.attribute)
        mocked_object.return_value()
        mocked_object.return_value.assert_called_with()

    def test_setting_return_value_in_constructor(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.Mock(return_value=return_value)
        self.assertEqual(mocked_object.return_value, return_value)
        self.assertEqual(mocked_object(), return_value)

    def test_arguments_passed_to_mock(self):
        mocked_object = unittest.mock.Mock(return_value=None)
        self.assertIsNone(mocked_object.call_args)

        mocked_object()
        self.assertEqual(mocked_object.call_args, unittest.mock.call())
        self.assertEqual(mocked_object.call_args, ())

        mocked_object(*POSITIONAL_ARGUMENTS)
        self.assertEqual(
            mocked_object.call_args,
            unittest.mock.call(*POSITIONAL_ARGUMENTS)
        )
        self.assertEqual(mocked_object.call_args, (POSITIONAL_ARGUMENTS,))
        self.assertEqual(mocked_object.call_args.args, POSITIONAL_ARGUMENTS)
        self.assertEqual(mocked_object.call_args.kwargs, {})

        args = (1, 2, 3, 4)
        kwargs = dict(a=1, b=2, c=3, n='N')
        mocked_object(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        self.assertEqual(
            mocked_object.call_args,
            unittest.mock.call(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)
        )
        self.assertEqual(mocked_object.call_args.args, args)
        self.assertEqual(mocked_object.call_args.kwargs, kwargs)

    def test_call_args_list(self):
        mocked_object = unittest.mock.Mock(return_value=None)

        mocked_object()
        mocked_object(POSITIONAL_ARGUMENTS)
        mocked_object(KEYWORD_ARGUMENTS)

        self.assertEqual(
            mocked_object.call_args_list,
            [
                unittest.mock.call(),
                unittest.mock.call(POSITIONAL_ARGUMENTS),
                unittest.mock.call(KEYWORD_ARGUMENTS),
            ]
        )

    def test_method_calls_track_all_calls_to_methods(self):
        mocked_object = unittest.mock.Mock()

        mocked_object.method()
        mocked_object.property.method.attribute()
        mocked_object.attribute_a
        mocked_object.attribute_b

        self.assertEqual(
            mocked_object.method_calls,
            [
                unittest.mock.call.method(),
                unittest.mock.call.property.method.attribute()
            ]
        )

    def test_class_attribute(self):
        self.assertIsInstance(unittest.mock.Mock(spec=3), int)
        self.assertIsInstance(unittest.mock.Mock(spec='3'), str)
        self.assertIsInstance(unittest.mock.Mock(spec=KEYWORD_ARGUMENTS), dict)