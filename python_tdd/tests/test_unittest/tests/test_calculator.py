import unittest
import calculator

class TestCalculator(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(
            calculator.add(2, 2),
            4
        )

    def test_subtraction(self):
        self.assertEqual(
            calculator.subtract(2, 2),
            0
        )

    def test_division(self):
        self.assertEqual(
            calculator.divide(2, 2),
            1
        )
        self.assertEqual(
            calculator.divide(2, 0),
            'You tried it'
        )

    def test_multiply(self):
        self.assertEqual(
            calculator.multiply(2, 2),
            4
        )