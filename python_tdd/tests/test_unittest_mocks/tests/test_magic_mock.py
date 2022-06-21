import unittest
import unittest.mock
import module


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