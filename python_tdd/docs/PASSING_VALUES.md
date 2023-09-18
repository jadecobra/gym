# How to pass values in python

We will step through passing values in python using Test Driven Development

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Passing Values

We can pass values to programs and use them in tests. Here's a test done with string interpolation

### <span style="color:red">**RED**</span>: make it fail

add a file named `test_passing_values.py` to the `tests` folder

```python
import unittest
import telephone


class TestPassingValues(unittest.TestCase):

    def test_text_messages(self):
        self.assertEqual(
            telephone.Telephone.text('hello'),
            'I received this message: hello'
        )
```
the terminal updates to show a [ModuleNotFoundError](./00_MODULE_NOT_FOUND_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- create a file named `telephone.py` in the project folder and the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- update `telephone.py` with a class definition
    ```python
    class Telephone(object):

        pass
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add a definition for an attribute named `text`
    ```python
    class Telephone(object):

        text = None
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md) because `text` is not callable
- change `text` to a method to make it callable
    ```python
    class Telephone(object):

        def text():
            return None
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md) because a positional argument was given in the caller, but the signature we defined does not take in any arguments
- update the definition for `text` to take in a value
    ```python
        def text(value):
            return None
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the return statement to make the test pass
    ```python
        def text(value):
            return 'I received this message: hello'
    ```
    the test passes

### <span style="color:orange">**REFACTOR**</span>: make it better

There's something wrong with this solution. No matter the value we send to the `text` method it will always return the same value. How can we make it return a value that is dependent on the input?

### <span style="color:red">**RED**</span>: make it fail

add a new test to `test_text_messages`

```python
        self.assertEqual(
            telephone.Telephone.text('yes'),
            'I received this message: yes'
        )
```

the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

We can add variable values to strings by using [string interpolation](https://peps.python.org/pep-0498/)

- update the `text` method in `telephone.py`
    ```python
    def text(value):
        return f'I received this message: {value}'
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's try it with other python data structures.

- update `test_text_messages` with a new test
    ```python
        self.assertEqual(
            telephone.Telephone.text(None),
            "I received this message: 'None'"
        )
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the test to match the expected value
    ```python
        self.assertEqual(
            telephone.Telephone.text(None),
            "I received this message: None"
        )
    ```
    the terminal updates to show a passing test
- add the following tests to `test_text_messages`
    ```python
        self.assertEqual(
            telephone.Telephone.text(bool),
            "I received this message: 'bool'"
        )
        self.assertEqual(
            telephone.Telephone.text(int),
            "I received this message: 'int'"
        )
        self.assertEqual(
            telephone.Telephone.text(float),
            "I received this message: 'float'"
        )
        self.assertEqual(
            telephone.Telephone.text(tuple),
            "I received this message: 'tuple'"
        )
        self.assertEqual(
            telephone.Telephone.text(list),
            "I received this message: 'list'"
        )
        self.assertEqual(
            telephone.Telephone.text(set),
            "I received this message: 'set'"
        )
        self.assertEqual(
            telephone.Telephone.text(dict),
            "I received this message: 'dict'"
        )
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the test to match the expected output
    ```python
        self.assertEqual(
            telephone.Telephone.text(bool),
            "I received this message: <class 'bool'>"
        )
    ```
    the terminal updates with an [AssertionError](./04_ASSERTION_ERROR.md) for the next test.
- repeat the above solution until all tests pass.

***VOILA***
We now know how to
- pass values
- represent values as strings using interpolation