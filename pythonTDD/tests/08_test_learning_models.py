import unittest


class TestInfiniteLearningModel(unittest.TestCase):
    def test_learning_model_when_expectations_are_greater_than_reality(self):
        "When our expectations are greater than reality we add to our reality until it exceeds expectations"
        expectations = 1
        reality = 0

        self.assertEqual(expectations + 1, learning.model(expectations, reality))

    def test_learning_model_when_expectations_are_less_than_reality(self):
        "When our expectations are less than reality we raise our expectations until it exceeds reality"
        expectations = 0
        reality = 1

        self.assertEqual(reality + 1, learning.model(expectations, reality))

    def test_learning_model_when_expectations_are_equal_to_reality(self):
        "When our expectations match reality we raise our expectations"
        expectations = 1
        reality = 1

        self.assertEqual(expectations + 1, learning.model(expectations, reality))


if __name__ == "__main__":
    unittest.main()
