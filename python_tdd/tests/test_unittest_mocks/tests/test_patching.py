import unittest
import unittest.mock
import module
import os

from tests.utilities import KEYWORD_ARGUMENTS, POSITIONAL_ARGUMENTS


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

    def test_patch_decorator(self):
        @unittest.mock.patch('module.ClassC')
        def function(arg, mock_class):
            return mock_class is module.ClassC

        self.assertTrue(function(None))
        self.assertTrue(function(int))
        self.assertTrue(function('bob'))

    def test_patch_as_context_manager(self):
        with unittest.mock.patch.object(module.Class, 'method', return_value=None) as mock_method:
            mocked_object = module.Class()
            mocked_object.method(module.function())
            mock_method.assert_called_once_with(module.function())

    def test_patching_with_return_values(self):
        return_value = 'return_value'
        with unittest.mock.patch('module.Class') as mocked_object:
            instance = mocked_object.return_value
            instance.method.return_value = return_value
            self.assertEqual(module.Class(), instance)
            self.assertEqual(module.Class().method(), return_value)

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

    def test_attach_mocks_with_names_using_patch(self):
        parent = unittest.mock.MagicMock()
        child_a = unittest.mock.MagicMock(return_value=None)
        child_b = unittest.mock.MagicMock(return_value=None)
        child_c = unittest.mock.MagicMock(return_value=None)
        child_n = unittest.mock.MagicMock(return_value=None)

        with  unittest.mock.patch('module.ClassA', return_value=None) as child_a:
            with unittest.mock.patch('module.ClassB', return_value=None) as child_b:
                parent.attach_mock(child_a, 'child_a')
                parent.attach_mock(child_b, 'child_b')
                parent.attach_mock(child_c, 'child_c')
                parent.attach_mock(child_n, 'child_n')

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

    def test_patching_with_spec(self):
        original = module.Class
        patcher = unittest.mock.patch('module.Class', spec=True)
        mocked_object = patcher.start()
        instance = mocked_object()
        self.assertIsInstance(instance, original)

    def test_patching_with_new_callable(self):
        original = module.Class()
        with unittest.mock.patch(
            'module.Class',
            new_callable=unittest.mock.NonCallableMock
        ) as mocked_object:
            self.assertNotEqual(original, mocked_object)

            with self.assertRaises(TypeError):
                original()

    def test_replace_an_object_with_io_string_io(self):
        import io

        @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
        def test(mock_stdout):
            print('Something')
            return mock_stdout.getvalue() == 'Something\n'

        self.assertTrue(test())

    def test_setting_attributes_in_constructor(self):
        mocked_object = unittest.mock.patch('module.Class', **KEYWORD_ARGUMENTS).start()
        self.assertEqual(mocked_object.a, 1)
        self.assertEqual(mocked_object.b, 2)
        self.assertEqual(mocked_object.c, 3)
        self.assertEqual(mocked_object.n, 'N')

    def test_patching_with_keyword_arguments(self):
        patcher = unittest.mock.patch(
            'module.ClassA',
            **{
                'method.return_value': 3,
                'other.side_effect': KeyError
            }
        )
        mocked_object = patcher.start()
        self.assertEqual(mocked_object.method(), 3)
        with self.assertRaises(KeyError):
            mocked_object.other()

    def test_patching_non_existent_attributes(self):
        import sys
        @unittest.mock.patch('sys.non_existent_attribute', 42)
        def test():
            return sys.non_existent_attribute == 42

        with self.assertRaises(AttributeError):
            test()

        @unittest.mock.patch('sys.non_existent_attribute', 42, create=True)
        def test():
            return sys.non_existent_attribute == 42

        self.assertTrue(test())

    def test_patching_dict_with_keyword_arguments(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.MagicMock()
        mocked_object.function.return_value = return_value

        with self.assertRaises(ModuleNotFoundError):
            import mocked_object

        with unittest.mock.patch.dict('sys.modules', mocked_object=mocked_object):
            import mocked_object
            self.assertEqual(
                mocked_object.function(*POSITIONAL_ARGUMENTS),
                return_value
            )

    def test_using_patch_dict_with_non_dictionaries(self):
        thing = module.Container()
        thing['one'] = 1
        with unittest.mock.patch.dict(thing, one=2, two=3):
            self.assertEqual(thing['one'], 2)
            self.assertEqual(thing['two'], 3)

        self.assertEqual(thing['one'], 1)
        self.assertEqual(list(thing), ['one'])

    def test_patch_multiple(self):
        @unittest.mock.patch.multiple(
            'module',
            ClassA=unittest.mock.DEFAULT,
            ClassB=unittest.mock.DEFAULT
        )
        def test(ClassA, ClassB):
            assert isinstance(ClassA, unittest.mock.MagicMock)
            assert isinstance(ClassB, unittest.mock.MagicMock)
        test()

    def test_patch_multiple_with_other_patchers(self):
        @unittest.mock.patch('sys.exit')
        @unittest.mock.patch.multiple(
            'module',
            ClassA=unittest.mock.DEFAULT,
            ClassB=unittest.mock.DEFAULT
        )
        def test(mock_exit, ClassA, ClassB):
            assert 'ClassA' in repr(ClassA)
            assert 'ClassB' in repr(ClassB)
            assert 'exit' in repr(mock_exit)
        test()

    def test_patch_multiple_as_context_manager(self):
        with unittest.mock.patch.multiple(
            'module',
            ClassA=unittest.mock.DEFAULT,
            ClassB=unittest.mock.DEFAULT
        ) as values:
            assert 'ClassA' in repr(values['ClassA'])
            assert 'ClassB' in repr(values['ClassB'])
            assert values['ClassA'] is module.ClassA
            assert values['ClassB'] is module.ClassB

    def test_patch_start_stop(self):
        patcher = unittest.mock.patch('module.ClassC')

        original = module.ClassC
        self.assertEqual(module.ClassC, original)

        new_mock = patcher.start()
        self.assertNotEqual(module.ClassC, original)
        self.assertEqual(module.ClassC, new_mock)

        patcher.stop()
        self.assertEqual(module.ClassC, original)
        self.assertNotEqual(module.ClassC, new_mock)


    def test_patching_builtins(self):
        @unittest.mock.patch('__main__.ord')
        def test(mock_ord):
            mock_ord.return_value = 101
            return ord('c')

        with self.assertRaises(AssertionError):
            self.assertEqual(test(), 101)






class TestSample(unittest.TestCase):

    def test_sample(self):
        with self.assertRaises(KeyError):
            self.assertEqual(os.environ['key'], 'value')


@unittest.mock.patch.dict('os.environ', {'key': 'value'})
class TestPatchingDictionaries(unittest.TestCase):

    def test_sample(self):
        self.assertEqual(os.environ['key'], 'value')


class TestPatchingInSetup(unittest.TestCase):

    def setUp(self):
        self.patcher1 = unittest.mock.patch('module.ClassA')
        self.patcher2 = unittest.mock.patch('module.ClassB')
        self.MockClassA = self.patcher1.start()
        self.MockClassB = self.patcher2.start()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_something(self):
        self.assertEqual(module.ClassA, self.MockClassA)
        self.assertEqual(module.ClassB, self.MockClassB)
