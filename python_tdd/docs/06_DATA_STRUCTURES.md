# Data Structures in python

This tutorial will cover data structures in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Data Structures

In programming we process input data of some form and output data in some form.
We can think of it as

```python
input_data -> program -> output_data
f(input_data) -> output_data # where f is the program|procress
```

## What are the data structures in python

- `None` - none - no value
- `bool` - boolean - True | False
- `int` - integers - positive/negative whole numbers e.g. -1, 0, 1
- `float` - floats - floating point numbers e.g. -1.1, 0.1, 1.1
- `str` - string - any text in strings"
- `tuple` - tuples - an immutable sequence of values
- `list` - lists - a mutable sequence of values
- `set` - sets - a sequence of values with no duplicates
- `dict` - dictionaries - a mapping of key, values

## What is None?

### <span style="color:red">**RED**</span>: Write a failing test

create a file named `test_data_structures.py` in the `tests` folder
```python
import unittest


class TestNone(unittest.TestCase):

    def test_none_is_none(self):
        self.assertIsNotNone(None)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: Make it Pass

update `test_none_is_none` to make the test pass
```python
        self.assertIsNone(None)
```
we assert what we learned in [04_ASSERTION_ERROR](04_ASSERTION_ERROR.md) that `None` is `None`

### <span style="color:orange">**REFACTOR**</span> - make it better

What other things can we compare with `None` to learn more about what it is or is not

### <span style="color:red">**RED**</span>: Write a failing test

add a new test to compare `None` with booleans
```python
    def test_is_none_a_boolean(self):
        self.assertIsNone(True)
        self.assertIsNone(False)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: Make it Pass

update `test_is_none_a_boolean` to make the tests pass
```python
        self.assertIsNotNone(True)
        self.assertIsNotNone(False)
```
we are reminded that
- `None` is `None`
- `True` is not `None`
- `False` is not `None`

### <span style="color:orange">**REFACTOR**</span> - make it better

booleans are represented by the keyword `bool` in python so we can do an instance test using another `unittest.TestCase` method that checks if an `object` is an instance of a `class`. We cover classes in [CLASSES](CLASSES.md)

### <span style="color:red">**RED**</span>: Write a failing test

update `test_is_none_a_boolean` with `self.assertIsInstance`
```python
    self.assertIsInstance(None, bool)
```
the terminal updates to show
```python
AssertionError: None is not an instance of <class 'bool'>
```
because `None` is not an instance of an integer

### <span style="color:green">**GREEN**</span>: Make it Pass

update `test_is_none_a_boolean` to make the test pass
```python
        self.assertNotIsInstance(None, bool)
```
We can summarize what we know about `None` so far
- `None` is `None`
- `None` is not a boolean

### <span style="color:orange">**REFACTOR**</span> - make it better

- What about other values in python?
- Is `None` equal to any `int`, `float`, `string`, `tuple`, `list`, `set` or `dict`?
Let's find out

### <span style="color:red">**RED**</span>: Write a failing test

add a new test to compare `None` with `int`
```python
    def test_is_none_an_integer(self):
        self.assertIsNone(-1)
        self.assertIsNone(0)
        self.assertIsNone(1)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: Make it Pass

update `test_is_none_an_integer` to make it pass
```python
        self.assertIsNotNone(-1)
        self.assertIsNotNone(0)
        self.assertIsNotNone(1)
```

### <span style="color:orange">**REFACTOR**</span> - make it better

integers are represented by the keyword `int` in python so we can do an instance test using another `unittest.TestCase` method that checks if an `object` is an instance of a `class`. We cover classes in [CLASSES](CLASSES.md)

### <span style="color:red">**RED**</span>: Write a failing test

update `test_is_none_an_integer` with `self.assertIsInstance`
```python
    self.assertIsInstance(None, int)
```
the terminal updates to show
```python
AssertionError: None is not an instance of <class 'int'>
```
because `None` is not an instance of an integer

### <span style="color:green">**GREEN**</span>: Make it Pass

update `test_is_none_an_integer` to make the test pass
```python
        self.assertNotIsInstance(None, int)
```

### <span style="color:orange">**REFACTOR**</span> - make it better
