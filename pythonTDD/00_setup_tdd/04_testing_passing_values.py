from unittest import TestCase
from telephone import Telephone


class TestPassingValues(TestCase):

	def test_text_messages(self):
		self.assertEqual(Telephone().text('hello'), 'i received this message: hello')
		self.assertEqual(Telephone().text('yes'), 'i received this message: yes')

	def test_phone_calls(self):
		self.assertEqual(Telephone().call(1234567890), 'did you mean to call: 1234567890')