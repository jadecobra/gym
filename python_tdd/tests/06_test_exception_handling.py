'''
Exceptions(Errors) break program execution
How can we test for errors?
How can we handle errors in our programs?
How can we design for failure?
'''

import unittest
import module
import exceptions


class TestExceptionHandling(unittest.TestCase):

    '''
    adding with self.assertRaises(ExceptionName):
    before an exception will ensure the exception was raised
    without stopping program execution
    e.g.
        with self.assertRaises(ModuleNotFoundError):
            import non_existent_module
    catches a ModuleNotFoundError
    '''

    def test_catching_module_not_found_error_exceptions_in_tests(self):
        import non_existent_module

    def test_catching_attribute_errors_in_tests(self):
        module.non_existent_attribute
        module.non_existent_function()
        module.NonExistentClass()
        module.Class.non_existent_attribute
        module.Class.non_existent_method()

    def test_catching_zero_division_error_in_tests(self):
        1 / 0

    def test_catching_exceptions(self):
        'Solve this before catching the error'
        exceptions.raises_exception_error()

    def test_catches_things_that_fail_0(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.raises_exception_error), "failed"
        )

    def test_catches_things_that_dont_fail_0(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.succeeding_function), "succeeded"
        )

    def test_catches_things_that_fail_1(self):
        self.assertEqual(
            exceptions.another_exception_handler(exceptions.raises_exception_error), "failed"
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
            exceptions.always_returns(exceptions.raises_exception_error),
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
