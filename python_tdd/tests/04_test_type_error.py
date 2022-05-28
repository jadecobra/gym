'''
TypeError can be raised when calling functions with the wrong number of inputs

Solve the errors below by creating functions with the right signatures
'''
import unittest
import functions


class TestTypeErrors(unittest.TestCase):
    def test_function_signatures_solve_type_errors(self):
        self.assertIsNone(functions.function_a("a"))
        self.assertIsNone(functions.function_b("a", "b"))
        self.assertIsNone(functions.function_c("a", "b", "c"))
        self.assertIsNone(functions.function_d("a", "b", "c", "d"))
        self.assertIsNone(functions.function_e(1, 2, 3, 4))
        self.assertIsNone(functions.function_f(1, 2, 3))
        self.assertIsNone(functions.function_g(1, 2))
        self.assertIsNone(functions.function_h(1))
        self.assertIsNone(functions.function_i(True))
        self.assertIsNone(functions.function_j(True, False))
        self.assertIsNone(functions.function_k(True, True, False))
        self.assertIsNone(functions.function_l(True, True, False, False))
        self.assertIsNone(functions.function_l(False, True, False, True))
        self.assertIsNone(functions.function_m(True, True, False))
        self.assertIsNone(functions.function_n(True, True))
        self.assertIsNone(functions.function_o(True))
        self.assertIsNone(functions.function_p(a=1))
        self.assertIsNone(functions.function_q(a=1, b=2))
        self.assertIsNone(functions.function_r(a=1, b=2, c=3))
        self.assertIsNone(functions.function_s(a=1, b=2, c=3, d=4))
        self.assertIsNone(functions.function_t(a=1, b=2, c=3, d=4))
        self.assertIsNone(functions.function_u(1, 2, a=3, b=4))
        self.assertIsNone(functions.function_v((1, 2), ("a", "b")))
        self.assertIsNone(functions.function_w([1, 2], ["a", "b"]))
        self.assertIsNone(functions.function_x({1, 2}, {"a", "b"}))
        self.assertIsNone(functions.function_y({"a": 1, "b": 2}, {1: "a", 2: "b"}))
        self.assertIsNone(functions.function_z(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
