import unittest
import unittest.mock
import module


class TestPatching(unittest.TestCase):

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
