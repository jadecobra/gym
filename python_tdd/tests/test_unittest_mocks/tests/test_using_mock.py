import asyncio
import unittest
import unittest.mock
import module
import datetime

from utilities import POSITIONAL_ARGUMENTS, KEYWORD_ARGUMENTS, RETURN_VALUE


class TestUsingMock(unittest.TestCase):

    def test_replacing_a_method_on_object(self):
        real_object = module.Class()
        real_object.method = unittest.mock.MagicMock()
        real_object.method(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)

    def test_example_tests(self):
        class Production:
            def method(self):
                self.something(POSITIONAL_ARGUMENTS)
            def something(self, *args):
                return None

        real_object = Production()
        real_object.something = unittest.mock.MagicMock()
        real_object.method()

        real_object.something.assert_called_once_with(POSITIONAL_ARGUMENTS)

    def test_mock_for_method_calls_on_an_object(self):
        class Production:
            def closer(self, something):
                something.close()

        real_object = Production()
        mock_object = unittest.mock.Mock()
        real_object.closer(mock_object)
        mock_object.close.assert_called_with()

    def test_mocking_classes(self):
        def function():
            instance = module.ClassA()
            return instance.method()

        return_value = 'return_value'
        with unittest.mock.patch('module.ClassA') as mock_object:
            mock_object.return_value.method.return_value = return_value
            self.assertEqual(function(), return_value)

    def test_naming_mocks(self):
        unittest.mock.MagicMock(name='foo')

    def test_tracking_all_calls(self):
        mock_object = unittest.mock.MagicMock()
        mock_object.method()
        mock_object.attribute.method(*POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS)

        self.assertEqual(
            mock_object.mock_calls,
            [
                unittest.mock.call.method(),
                unittest.mock.call.attribute.method(
                    *POSITIONAL_ARGUMENTS, **KEYWORD_ARGUMENTS
                )
            ]
        )

    def test_tracking_nested_calls_is_impossible(self):
        mock_object = unittest.mock.Mock()
        mock_object.factory(important=True).deliver()
        self.assertEqual(
            mock_object.mock_calls,
            [
                unittest.mock.call.factory(important=True),
                unittest.mock.call.factory().deliver()
            ]
        )

        self.assertEqual(
            mock_object.mock_calls[-1],
            unittest.mock.call.factory(importance=False).deliver()
        )

    def test_setting_return_values_on_a_mock_attribute(self):
        mock_object = unittest.mock.Mock()
        mock_object.return_value = RETURN_VALUE
        self.assertEqual(mock_object(), RETURN_VALUE)

    def test_setting_return_values_on_methods(self):
        mock_object = unittest.mock.Mock()
        mock_object.method.return_value = RETURN_VALUE
        self.assertEqual(mock_object.method(), RETURN_VALUE)

    def test_setting_return_value_in_constructor(self):
        mock_object = unittest.mock.Mock(return_value=RETURN_VALUE)
        self.assertEqual(mock_object(), RETURN_VALUE)

    def test_setting_an_attribute_on_a_mock(self):
        mock_object = unittest.mock.Mock()
        mock_object.attribute = RETURN_VALUE
        self.assertEqual(mock_object.attribute, RETURN_VALUE)

    def test_asserting_chained_calls(self):
        mock_object = unittest.mock.Mock()
        cursor = mock_object.connection.cursor.return_value
        cursor.execute.return_value = list(POSITIONAL_ARGUMENTS)
        self.assertEqual(
            mock_object.connection.cursor().execute('SELECT 1'),
            list(POSITIONAL_ARGUMENTS)
        )

        self.assertEqual(
            mock_object.mock_calls,
            unittest.mock.call.connection.cursor().execute("SELECT 1").call_list()
        )

    def test_raising_exceptions_with_mocks(self):
        mock_object = unittest.mock.Mock(side_effect=Exception('BOOM'))
        with self.assertRaises(Exception):
            mock_object()

    def test_setting_side_effect_to_an_iterable(self):
        mock_object = unittest.mock.MagicMock(side_effect=POSITIONAL_ARGUMENTS)
        self.assertEqual(mock_object(), 1)
        self.assertEqual(mock_object(), 2)
        self.assertEqual(mock_object(), 3)
        self.assertEqual(mock_object(), 4)
        with self.assertRaises(StopIteration):
            mock_object()

    def test_setting_side_effect_to_a_function(self):
        def side_effect(*args):
            return {(1, 2): 1, (2, 3): 2}[args]

        mock_object = unittest.mock.MagicMock(side_effect=side_effect)
        self.assertEqual(mock_object(1, 2), 1)
        self.assertEqual(mock_object(2, 3), 2)

    def test_mocking_asynchronous_iterators(self):
        mock_object = unittest.mock.MagicMock()
        mock_object.__aiter__.return_value = POSITIONAL_ARGUMENTS

        async def test():
            return [i async for i in mock_object]

        asyncio.run(test())

    def test_mocking_asynchronous_context_manager(self):
        class AsyncContextManager:
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, traceback):
                return None

        mock_object = unittest.mock.MagicMock(AsyncContextManager())

        async def test():
            async with mock_object as result:
                return None

        asyncio.run(test())
        mock_object.__aenter__.assert_awaited_once()
        mock_object.__aexit__.assert_awaited_once()

    def test_creating_a_mock_from_an_existing_object(self):
        mock_object = unittest.mock.Mock(spec=module.Class)
        with self.assertRaises(AttributeError):
            mock_object.old_method()

    