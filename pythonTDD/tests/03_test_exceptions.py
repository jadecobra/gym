import unittest
import exceptions

class TestExceptionHandling(unittest.TestCase):

    def test_catching_exceptions_in_tests(self):
        with self.assertRaises(ZeroDivisionError):
            1/0

    def test_catching_exceptions(self):
        with self.assertRaises(Exception):
            exceptions.raises_exception_error()

    def test_catches_things_that_fail_0(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.raises_exception),
            'failed'
        )

    def test_catches_things_that_dont_fail_0(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.succeeding_function),
            'succeeded'
        )

    def test_catches_things_that_fail_1(self):
        self.assertEqual(
            exceptions.another_exception_handler(exceptions.raises_exception),
            'failed'
        )

    def test_catches_things_that_dont_fail_1(self):
        self.assertEqual(
            exceptions.another_exception_handler(exceptions.succeeding_function),
            'succeeded'
        )

    def test_finally_always_returns(self):
        self.assertEqual(
            exceptions.always_returns(exceptions.succeeding_function),
            'always_returns_this'
        )
        self.assertEqual(
            exceptions.always_returns(exceptions.raises_exception),
            'always_returns_this'
        )

    def test_catching_explicit_errors(self):
        self.assertEqual(
            exceptions.zero_division_catcher(ZeroDivisionError),
            'caught_zero_division_error'
        )
        with self.assertRaises(TypeError):
            exceptions.zero_division_catcher(TypeError)

        with self.assertRaises(AttributeError):
            exceptions.zero_division_catcher(AttributeError)

        with self.assertRaises(Exception):
            exceptions.zero_division_catcher(Exception)

    def test_catching_explicit_errors_with_finally(self):
        self.assertEqual(
            exceptions.zero_division_catcher_with_finally(ZeroDivisionError),
            'caught_zero_division_error'
        )
        self.assertEqual(
            exceptions.zero_division_catcher_with_finally(TypeError),
            'caught_nothing'
        )
        self.assertEqual(
            exceptions.zero_division_catcher_with_finally(AttributeError),
            'caught_nothing'
        )
        self.assertEqual(
            exceptions.zero_division_catcher_with_finally(Exception),
            'caught_nothing'
        )

    def test_catching_specific_errors(self):
        self.assertEqual(
            str(exceptions.error_catcher(ZeroDivisionError)),
            str(ZeroDivisionError())
        )


if __name__ == "__main__":
    unittest.main()