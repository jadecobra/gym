from unittest import TestCase
from exceptions import (
	raises_exception_error, exception_handler,
	raises_exception, succeeding_function,
	another_exception_handler, always_returns, error_catcher, zero_division_catcher, zero_division_catcher_with_finally
)


class TestExceptionHandling(TestCase):

	def test_catching_exceptions_in_tests(self):
		with self.assertRaises(ZeroDivisionError):
			1/0

	def test_catching_exceptions(self):
		with self.assertRaises(Exception):
			raises_exception_error()

	# def test_all_errors_inherit_from_exception_class(self):
	# 	self.assertIsInstance(ConnectionError, BrokenPipeError)

	def test_catches_things_that_fail_0(self):
		self.assertEqual(
			exception_handler(raises_exception),
			'failed'
		)

	def test_catches_things_that_dont_fail_0(self):
		self.assertEqual(
			exception_handler(succeeding_function),
			'succeeded'
		)

	def test_catches_things_that_fail_1(self):
		self.assertEqual(
			another_exception_handler(raises_exception),
			'failed'
		)

	def test_catches_things_that_dont_fail_1(self):
		self.assertEqual(
			another_exception_handler(succeeding_function),
			'succeeded'
		)

	def test_finally_always_returns(self):
		self.assertEqual(
			always_returns(succeeding_function),
			'always_returns_this'
		)
		self.assertEqual(
			always_returns(raises_exception),
			'always_returns_this'
		)

	def test_catching_explicit_errors(self):
		self.assertEqual(
			zero_division_catcher(ZeroDivisionError),
			'caught_zero_division_error'
		)
		with self.assertRaises(TypeError):
			zero_division_catcher(TypeError)
		with self.assertRaises(AttributeError):
			zero_division_catcher(AttributeError)
		with self.assertRaises(Exception):
			zero_division_catcher(Exception)

	def test_catching_explicit_errors_with_finally(self):
		self.assertEqual(
			zero_division_catcher_with_finally(ZeroDivisionError),
			'caught_zero_division_error'
		)
		self.assertEqual(
			zero_division_catcher_with_finally(TypeError),
			'caught_nothing'
		)
		self.assertEqual(
			zero_division_catcher_with_finally(AttributeError),
			'caught_nothing'
		)
		self.assertEqual(
			zero_division_catcher_with_finally(Exception),
			'caught_nothing'
		)

	def test_catching_specific_errors(self):
		self.assertEqual(
			str(error_catcher(ZeroDivisionError)),
			str(ZeroDivisionError())
		)
