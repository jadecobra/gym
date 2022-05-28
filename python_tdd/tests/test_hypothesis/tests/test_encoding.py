import unittest
import os
import encoding
import hypothesis


class TestEncoding(unittest.TestCase):
    @hypothesis.given(hypothesis.strategies.text())
    def test_encoding(self, a_string):
        self.assertEqual(encoding.decode(encoding.encode(a_string)), a_string)

    @hypothesis.given(a_string=hypothesis.strategies.text())
    @hypothesis.example(a_string="")
    def test_encoding_with_example(self, a_string):
        self.assertEqual(encoding.decode(encoding.encode(a_string)), a_string)
