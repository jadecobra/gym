import unittest
import learning


class TestInfiniteLearningModel(unittest.TestCase):
    def test_learning_model_when_expectations_are_greater_than_reality(self):
        "When expectations exceed reality, add to reality until it exceeds expectations"
        expectations = 1
        reality = 0

        self.assertEqual(expectations + 1, learning.model(expectations, reality))

    def test_learning_model_when_expectations_are_less_than_reality(self):
        "When reality exceeds expectations, add to expectations until it exceeds reality"
        expectations = 0
        reality = 1

        self.assertEqual(reality + 1, learning.model(expectations, reality))

    def test_learning_model_when_expectations_are_equal_to_reality(self):
        "When expectations equal reality, raise expectations"
        expectations = 1
        reality = 1

        self.assertEqual(expectations + 1, learning.model(expectations, reality))


if __name__ == "__main__":
    unittest.main()
