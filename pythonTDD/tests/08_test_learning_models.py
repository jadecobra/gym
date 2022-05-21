import unittest
import random
import learning


class TestInfiniteLearningModel(unittest.TestCase):
    def test_learning_model_when_expectations_are_greater_than_reality(self):
        "When expectations exceed reality, add to reality until it exceeds expectations"
        reality = random.random()
        expectations = reality + 1
        self.assertGreater(learning.model(expectations, reality), expectations)

    def test_learning_model_when_expectations_are_less_than_reality(self):
        "When reality exceeds expectations, add to expectations until it exceeds reality"
        reality = random.random()
        expectations = reality - 1
        self.assertGreater(learning.model(expectations, reality), reality)

    def test_learning_model_when_expectations_are_equal_to_reality(self):
        "When expectations equal reality, raise expectations"
        reality = random.random()
        expectations = reality
        self.assertGreater(learning.model(expectations, reality), expectations)


if __name__ == "__main__":
    unittest.main()
