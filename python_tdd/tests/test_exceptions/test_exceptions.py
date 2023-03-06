import unittest



class TestExceptionHandling(unittest.TestCase):

    def test_zero_division_error(self):
        with self.assertRaises(ZeroDivisionError):
            10 * (1 / 0)

    def test_name_error(self):
        with self.assertRaises(NameError):
            4 + spam * 3

    def test_type_error(self):
        with self.assertRaises(TypeError):
            '2' + 2

    