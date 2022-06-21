from multiprocessing import parent_process
import unittest
import unittest.mock
import module


MOCKED_CLASS = module.Class()
MOCKED_CLASS.method = unittest.mock.MagicMock(return_value=module.function())


class TestUnittestMock(unittest.TestCase):

    def test_failure(self):
        self.assertEqual(
            MOCKED_CLASS.method(module.function()),
            module.function()
        )

    def test_assert_called_with(self):
        with self.assertRaises(AssertionError):
            MOCKED_CLASS.method.assert_called_with(module.function())

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

    @unittest.mock.patch('module.ClassB')
    @unittest.mock.patch('module.ClassA')
    def test_patching_decorator(self, MockClass1, MockClass2):
        module.ClassA()
        module.ClassB()
        self.assertEqual(MockClass1, module.ClassA)
        self.assertEqual(MockClass2, module.ClassB)
        self.assertTrue(MockClass1.called)
        self.assertTrue(MockClass2.called)

    def test_patch_as_context_manager(self):
        with unittest.mock.patch.object(module.Class, 'method', return_value=None) as mock_method:
            mocked_object = module.Class()
            mocked_object.method(module.function())
            mock_method.assert_called_once_with(module.function())

    def test_patch_as_context_manager_with_non_existent_method(self):
        with self.assertRaises(AttributeError):
            with unittest.mock.patch.object(
                module.Class, 'non_existent_method', return_value=None
            ) as mock_method:
                module.Class()

    def test_setting_values_in_dictionary_during_test_scope(self):
        original_dict = {
            'A': 1,
            'B': 2,
            'C': 3,
            'N': 'N',
        }
        mocked_dict = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
        }
        with unittest.mock.patch.dict(original_dict, mocked_dict, clear=True):
            self.assertEqual(original_dict, mocked_dict)
        self.assertNotEqual(original_dict, mocked_dict)

    def test_patching_magic_methods(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.MagicMock()
        mocked_object.__str__.return_value = return_value
        self.assertEqual(str(mocked_object), return_value)
        mocked_object.__str__.assert_called_with()

    def test_magic_methods_with_mock_class(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.Mock()
        mocked_object.__str__ = unittest.mock.Mock(return_value=return_value)
        self.assertEqual(str(mocked_object), return_value)

    def test_ensuring_mock_has_same_api_as_original(self):
        return_value = 'return_value'
        mock_function = unittest.mock.create_autospec(
            module.function_with_positional_arguments,
            return_value=return_value
        )
        self.assertEqual(mock_function(1, 2, 3), return_value)
        mock_function.assert_called_once_with(1, 2, 3)
        self.assertNotEqual(
            mock_function(1, 2, 3),
            module.function_with_positional_arguments(1, 2, 3)
        )
        with self.assertRaises(TypeError):
            mock_function('invalid argument')
            module.function('invalid argument')