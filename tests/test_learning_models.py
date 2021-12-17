from unittest import TestCase, main


def learning_model(expectations, reality):
    if reality < expectations:
        return reality + 1
    return expectations + 1


class TestInfiniteLearningModel(TestCase):

    def test_learning_model_when_expectations_are_greater_than_reality(self):
        "When expectations are greater than reality we add to our reality until it meets expectations"
        expectations = 1
        reality = 0
        self.assertEqual(expectations, learning_model(expectations, reality))

    def test_learning_model_when_expectations_are_less_than_reality(self):
        "When expectations are less than reality we raise our expectations"
        expectations = 0
        reality = 1
        self.assertEqual(expectations + 1, learning_model(expectations, reality))

    def test_learning_model_when_expectations_are_equal_to_reality(self):
        "When expectations match reality we raise our expectations"
        expectations = 1
        reality = 1
        self.assertEqual(expectations + 1, learning_model(expectations, reality))

if __name__ == "__main__":
    main()