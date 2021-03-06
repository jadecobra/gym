import unittest
import unittest.mock
import module

from utilities import POSITIONAL_ARGUMENTS, KEYWORD_ARGUMENTS

MOCKED_CLASS = module.Class()
MOCKED_CLASS.method = unittest.mock.MagicMock(return_value=module.function())



class TestUnittestMagicMock(unittest.TestCase):

    def test_failure(self):
        self.assertEqual(
            MOCKED_CLASS.method(module.function()),
            module.function()
        )

    def test_assert_called_with(self):
        with self.assertRaises(AssertionError):
            MOCKED_CLASS.method.assert_called_with(module.function())

    def test_patching_magic_methods(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.MagicMock()
        mocked_object.__str__.return_value = return_value
        self.assertEqual(str(mocked_object), return_value)
        mocked_object.__str__.assert_called_with()

    def test_mock_calls_records_all_calls_to_object(self):
        mocked_object = unittest.mock.MagicMock()

        mocked_object(POSITIONAL_ARGUMENTS)
        mocked_object(KEYWORD_ARGUMENTS)
        mocked_object.first(a=3)
        mocked_object.second()
        self.assertEqual(int(mocked_object), 1)

        self.assertEqual(
            mocked_object.mock_calls,
            [
                unittest.mock.call(POSITIONAL_ARGUMENTS),
                unittest.mock.call(KEYWORD_ARGUMENTS),
                unittest.mock.call.first(a=3),
                unittest.mock.call.second(),
                unittest.mock.call.__int__(),
            ]
        )

    def test_nested_mock_calls(self):
        mocked_object = unittest.mock.MagicMock()
        mocked_object.top(a=3).bottom()

        self.assertEqual(
            mocked_object.mock_calls,
            [
                unittest.mock.call.top(a=3),
                unittest.mock.call.top().bottom()
            ]
        )

    def test_setting_arbitrary_attributes_in_constructor(self):
        mocked_object = unittest.mock.MagicMock(
            attribute_a=1,
            attribute_b=2,
            attribute_c=3,
            attribute_n='N'
        )
        self.assertEqual(mocked_object.attribute_a, 1)
        self.assertEqual(mocked_object.attribute_b, 2)
        self.assertEqual(mocked_object.attribute_c, 3)
        self.assertEqual(mocked_object.attribute_n, 'N')

    def test_deleting_attributes(self):
        mocked_object = unittest.mock.MagicMock()

        self.assertTrue(hasattr(mocked_object, 'mocked_attribute'))

        del mocked_object.mocked_attribute
        self.assertFalse(hasattr(mocked_object, 'mocked_attribute'))

        del mocked_object.non_existent_attribute
        with self.assertRaises(AttributeError):
            mocked_object.non_existent_attribute

    def test_set_name_attribute_with_configure_mock(self):
        mocked_object = unittest.mock.MagicMock()
        mocked_object.configure_mock(name='mocked_object')
        self.assertEqual(
            mocked_object.name, 'mocked_object'
        )

    def test_set_name_attribute_with_assignment(self):
        mocked_object = unittest.mock.MagicMock()
        mocked_object.name = 'mocked_object'
        self.assertEqual(
            mocked_object.name, 'mocked_object'
        )

    def test_attaching_mocks_as_attributes(self):
        parent = unittest.mock.MagicMock()
        child_a = unittest.mock.MagicMock(return_value=None)
        child_b = unittest.mock.MagicMock(return_value=None)
        child_c = unittest.mock.MagicMock(return_value=None)
        child_n = unittest.mock.MagicMock(return_value=None)

        parent.child_a = child_a
        parent.child_b = child_b
        parent.child_c = child_c
        parent.child_n = child_n

        child_a(1)
        child_b(2)
        child_c(3)
        child_n('N')

        self.assertEqual(
            parent.mock_calls,
            [
                unittest.mock.call.child_a(1),
                unittest.mock.call.child_b(2),
                unittest.mock.call.child_c(3),
                unittest.mock.call.child_n('N')
            ]
        )

    def test_attaching_mocks_with_names(self):
        mocked_object = unittest.mock.MagicMock()
        not_a_child = unittest.mock.MagicMock(name='not_a_child')
        mocked_object.attribute = not_a_child
        mocked_object.attribute()

        self.assertEqual(mocked_object.mock_calls, [])

    def test_mocking_magic_methods_with_functions(self):
        def __str__(self):
            return 'fooble'
        mocked_object = unittest.mock.Mock()
        mocked_object.__str__ = __str__
        self.assertEqual(str(mocked_object), 'fooble')

    def test_mocking_magic_methods_with_return_value(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.Mock()
        mocked_object.__str__ = unittest.mock.Mock()
        mocked_object.__str__.return_value = return_value
        self.assertEqual(str(mocked_object), return_value)

    def test_mocking_magic_methods_with_mock_constructor_return_value(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.__iter__ = unittest.mock.Mock(return_value=iter(POSITIONAL_ARGUMENTS))
        self.assertEqual(
            list(mocked_object),
            [*POSITIONAL_ARGUMENTS]
        )

    def test_mocking_objects_used_as_context_managers(self):
        mocked_object = unittest.mock.Mock()
        mocked_object.__enter__ = unittest.mock.Mock(return_value='foo')
        mocked_object.__exit__ = unittest.mock.Mock(return_value=False)

        with mocked_object as m:
            assert m == 'foo'

        mocked_object.__enter__.assert_called_with()
        mocked_object.__exit__.assert_called_with(None, None, None)

    def test_magic_methods_are_setup_with_magic_mock_objects(self):
        mocked_object = unittest.mock.MagicMock()
        mocked_object[3] = 'fish'
        mocked_object.__setitem__.assert_called_with(3, 'fish')
        mocked_object.__getitem__.return_value = 'return_value'
        self.assertEqual(mocked_object[2], 'return_value')

    def test_magic_methods_and_their_defaults(self):
        mocked_object = unittest.mock.MagicMock()
        self.assertEqual(int(mocked_object), 1)
        self.assertEqual(len(mocked_object), 0)
        self.assertEqual(list(mocked_object), [])
        self.assertFalse(object() in mocked_object)
        self.assertTrue(bool(mocked_object))

    def test_equality_methods(self):
        mocked_object = unittest.mock.MagicMock()
        self.assertNotEqual(mocked_object, 3)
        mocked_object.__eq__.return_value = True
        self.assertEqual(mocked_object, 3)

    def test_iter(self):
        mocked_object = unittest.mock.MagicMock()
        mocked_object.__iter__.return_value = POSITIONAL_ARGUMENTS
        self.assertEqual(list(mocked_object), list(POSITIONAL_ARGUMENTS))
        self.assertEqual(list(mocked_object), list(POSITIONAL_ARGUMENTS))

    def test_iterator_return_values(self):
        mocked_object = unittest.mock.MagicMock()
        mocked_object.__iter__.return_value = iter(POSITIONAL_ARGUMENTS)
        self.assertEqual(list(mocked_object), list(POSITIONAL_ARGUMENTS))
        self.assertEqual(list(mocked_object), [])
