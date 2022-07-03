import unittest
import unittest.mock
import urllib.request
import module


class TestAutoSpeccing(unittest.TestCase):

    def test_speccing(self):
        patcher = unittest.mock.patch('urllib.request', autospec=True)
        mock_urllib_request = patcher.start()
        self.assertEqual(
            urllib.request,
            mock_urllib_request
        )

        with self.assertRaises(TypeError):
            urllib.request.Request()
            mock_urllib_request.Request()

        request = urllib.request.Request('foo')
        self.assertIsInstance(
            request,
            unittest.mock.NonCallableMagicMock
        )

        self.assertIsInstance(
            request.add_header('spam', 'eggs'),
            unittest.mock.MagicMock
        )

        with self.assertRaises(AttributeError):
            request.assret_called_with

    def test_create_autospec(self):
        mock_request = unittest.mock.create_autospec(urllib.request)
        with self.assertRaises(TypeError):
            mock_request.Request()

    def test_autospeccing_when_attributes_defined_in_init(self):
        with unittest.mock.patch('module.ClassE', autospec=True):
            instance = module.ClassE()
            with self.assertRaises(AttributeError):
                instance.attribute

    def test_setting_dynamic_attributes_with_autospecced_objects(self):
        with unittest.mock.patch('module.ClassE', autospec=True):
            instance = module.Class()
            instance.method = 33
            self.assertEqual(instance.method, 33)
