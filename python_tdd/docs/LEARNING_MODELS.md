# How can we tell if we are learning something?

Congratulations! You have journeyed with me through some exercises to help you get more familiar with Test Driven Development and Python. What follows is an exercise in measuring learning. It is somewhat philosophical in its meaning but arithmetic in its representation. I am curious to know what you think and what solutions you come up with

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## An Infinite Learning Model

### <span style="color:red">**RED**</span>: make it fail

add a file named `test_learning_models.py` to the `tests` folder with the following contents

```python
import unittest
import learning


class TestInfiniteLearningModel(unittest.TestCase):

    def test_learning_model_when_expectations_greater_than_reality(self):
        '''When expectations are greater than reality,
        increase reality until it is greater than expectations'''

        reality = 0
        expectations = reality + 1

        self.assertGreater(
            learning.model(expectations, reality),
            expectations
        )

    def test_learning_model_when_expectations_less_than_reality(self):
        '''When expectations are less than reality,
        increase expectations until they are greater than reality'''

        reality = 1
        expectations = reality - 1

        self.assertGreater(
            learning.model(expectations, reality),
            reality
        )

    def test_learning_model_when_expectations_equal_to_reality(self):
        '''When expectations equal reality, increase expectations'''

        reality = 1
        expectations = reality

        self.assertGreater(
            learning.model(expectations, reality),
            expectations
        )
```

### <span style="color:green">**GREEN**</span>: make it pass

If you've gone through any of the other exercises in this book, then you have what you need to solve these problems

### <span style="color:orange">**REFACTOR**</span>: make it better

Please send me your solutions. I am curious to see them. Enjoy