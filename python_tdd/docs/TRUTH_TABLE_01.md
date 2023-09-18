# How to write conditions in python

We will step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

We know that there are two boolean values
- `True`
- `False`

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Nullary Operations

These operations take in no inputs and always return the same value. They are singleton [functions](./07_FUNCTIONS.md)

### <span style="color:red">**RED**</span>: make it fail

create a file named `test_truth_table.py` in the `tests` folder and add the following

```python
import unittest
import truth_table


class TestNullaryOperations(unittest.TestCase):

    def test_logical_true(self):
        self.assertTrue(truth_table.logical_true())
```
the terminal updates to show a [ModuleNotFoundError](./00_MODULE_NOT_FOUND_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- create a module named `truth_table.py` and the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add a singleton function named `logical_true`
    ```python
    def logical_true():
        return True
    ```
    the terminal updates to show passing tests
- We are reminded that `True` is `True`

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's add a test for `logical_false`

- add a test to `TestNullaryOperations`
    ```python
    def test_logical_false(self):
        self.assertFalse(truth_table.logical_false())
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add a function definition to `truth_table.py`
    ```python
    def logical_false():
        return True
    ```
    the terminal shows an [AssertionError](./04_ASSERTION_ERROR.md)
- update the return value to `False` and the terminal updates to show passing tests
    ```python
    def logical_false():
        return False
    ```
- We are again reminded that
    - `False` is `False`
    - `True` is `True`


## Unary Operations

These take in one input and return the input, they are passthrough [functions](./07_FUNCTIONS.md)
### Logical Identity

#### <span style="color:red">**RED**</span>: make it fail

We add a new `TestCase` to `test_truth_table.py`

```python


class TestUnaryOperations(unittest.TestCase):

    def test_logical_identity(self):
        self.assertTrue(truth_table.logical_identity(True))
        self.assertFalse(truth_table.logical_identity(False))
```

the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

add a function definition to `truth_table.py`
```python
def logical_identity(value):
    return value
```
the terminal updates to show passing tests

### Logical Negation

#### <span style="color:red">**RED**</span>: make it fail

add a test for `logical_negation`
```python
    def test_logical_negation(self):
        self.assertFalse(truth_table.logical_negation(True))
        self.assertTrue(truth_table.logical_negation(False))
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- update `truth_table.py` with a definition for `logical_negation`
    ```python
    def logical_negation(value):
        return value
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md). The `logical_negation` function returns the value it receives as input.
- How do we make the function return the opposite of what it receives? use the `not` keyword. update `logical_negation` to return the opposite of the `bool` value it returns
    ```python
    def logical_negation(value):
        return not value
    ```
    the terminal updates to show passing tests

Reviewing what we know so far
    - `True` is `not False`
    - `False` is `not True`
    - `False` is `False`
    - `True` is `True`