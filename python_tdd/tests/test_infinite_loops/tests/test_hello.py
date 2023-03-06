import unittest
import infinite_hello


class TestInfiniteHello(unittest.TestCase):

    def test_infinite_hello_raises_recursion_error(self):
        with self.assertRaises(RecursionError):
            infinite_hello.hello('hello')