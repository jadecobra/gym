'''
Exceptions(Errors) break program execution
How can we test for errors?
How can we handle errors in our programs?
How can we design for failure?
'''

import unittest
import exceptions
import module


class TestExceptionHandling(unittest.TestCase):
    def test_catching_exceptions_in_tests(self):
        with self.assertRaises(ModuleNotFoundError):
            import non_existent_module
        with self.assertRaises(AttributeError):
            module.non_existent_attribute
        with self.assertRaises(AttributeError):
            module.non_existent_function()
        with self.assertRaises(AttributeError):
            module.NonExistentClass()
        with self.assertRaises(AttributeError):
            module.Class.non_existent_attribute
        with self.assertRaises(AttributeError):
            module.Class.non_existent_method()
        with self.assertRaises(ZeroDivisionError):
            1 / 0

    def test_catching_exceptions(self):
        with self.assertRaises(Exception):
            exceptions.raises_exception_error()

    def test_catches_things_that_fail_0(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.raises_exception), "failed"
        )

    def test_catches_things_that_dont_fail_0(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.succeeding_function), "succeeded"
        )

    def test_catches_things_that_fail_1(self):
        self.assertEqual(
            exceptions.another_exception_handler(exceptions.raises_exception), "failed"
        )

    def test_catches_things_that_dont_fail_1(self):
        self.assertEqual(
            exceptions.another_exception_handler(exceptions.succeeding_function),
            "succeeded",
        )

    def test_finally_always_returns(self):
        self.assertEqual(
            exceptions.always_returns(exceptions.succeeding_function),
            "always_returns_this",
        )
        self.assertEqual(
            exceptions.always_returns(exceptions.raises_exception),
            "always_returns_this",
        )

    def test_catching_explicit_errors(self):
        self.assertEqual(
            exceptions.zero_division_catcher(ZeroDivisionError),
            "caught_zero_division_error",
        )
        with self.assertRaises(TypeError):
            exceptions.zero_division_catcher(TypeError)

        with self.assertRaises(AttributeError):
            exceptions.zero_division_catcher(AttributeError)

        with self.assertRaises(Exception):
            exceptions.zero_division_catcher(Exception)

    def test_catching_multiple_errors(self):
        self.assertEqual(
            exceptions.multiple_errors_catcher(TypeError),
            "caught an exception"
        )
        self.assertEqual(
            exceptions.multiple_errors_catcher(ZeroDivisionError),
            "caught an exception"
        )
        with self.assertRaises(AttributeError):
            exceptions.multiple_errors_catcher(AttributeError)

if __name__ == "__main__":
    unittest.main()
