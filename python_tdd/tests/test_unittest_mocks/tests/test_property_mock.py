import unittest
import unittest.mock
import module

from utilities import POSITIONAL_ARGUMENTS, KEYWORD_ARGUMENTS


class TestPropertyMock(unittest.TestCase):

    def test_mocking_properties(self):
        self.assertEqual(module.ClassD().attribute, 'attribute')

        return_value = 'return_value'

        with unittest.mock.patch(
            'module.ClassD.attribute',
            new_callable=unittest.mock.PropertyMock
        ) as mocked_attribute:
            mocked_attribute.return_value = return_value
            original_object = module.ClassD()
            self.assertEqual(original_object.attribute, return_value)
            self.assertEqual(mocked_attribute.mock_calls, [unittest.mock.call()])

            original_object.attribute = 6
            self.assertEqual(mocked_attribute.mock_calls, [
                unittest.mock.call(),
                unittest.mock.call(6)
            ])

    def test_attaching_a_property_mock(self):
        return_value = 'return_value'
        mocked_object = unittest.mock.MagicMock()
        mocked_property = unittest.mock.PropertyMock(return_value=return_value)
        type(mocked_object).mocked_property = mocked_property

        self.assertEqual(mocked_object.mocked_property, return_value)
        mocked_property.assert_called_once_with()

