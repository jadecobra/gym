"How do I know I am learning?"
import unittest
import learning


class TestInfiniteLearningModel(unittest.TestCase):
    
    def test_learning_model_when_expectations_greater_than_reality(self):
        "When expectations exceed reality, update reality to exceed expectations"
        reality = 0
        expectations = reality + 1
        self.assertGreater(learning.model(expectations, reality), expectations)

    def test_learning_model_when_expectations_less_than_reality(self):
        "When reality exceeds expectations, update expectations to exceed reality"
        reality = 1
        expectations = reality - 1
        self.assertGreater(learning.model(expectations, reality), reality)

    def test_learning_model_when_expectations_equal_to_reality(self):
        "When expectations equal reality, raise expectations"
        reality = 1
        expectations = reality
        self.assertGreater(learning.model(expectations, reality), expectations)


if __name__ == "__main__":
    unittest.main()
