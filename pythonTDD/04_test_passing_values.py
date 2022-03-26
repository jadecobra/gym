import unittest
import telephone


class TestPassingValues(unittest.TestCase):

    def test_text_messages(self):
        self.assertEqual(
            telephone.Telephone().text('hello'),
            'I received this message: hello'
        )
        self.assertEqual(
            telephone.Telephone().text('yes'),
            'I received this message: yes'
        )

    def test_phone_calls(self):
        self.assertEqual(
            telephone.Telephone().call(1234567890),
            'Helloooo! did you mean to call: 1234567890'
        )
