# None

This tutorial will cover `None` in python using Test Driven Development

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
- `list` - lists | arrays - a mutable sequence of values
- `set` - sets - a sequence of values with no duplicates
- `dict` - dictionaries - a mapping of key, values

## What is None?

`None` is an object used to represent the absence of a value

### <span style="color:red">**RED**</span>: make a failing test

create a file named `test_data_structures.py` in the `tests` folder
```python
import unittest


class TestDataStructures(unittest.TestCase):

    def test_none_is_none(self):
        self.assertIsNotNone(None)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

update `test_none_is_none` to make the test pass
```python
        self.assertIsNone(None)
```
we assert what we learned in [04_ASSERTION_ERROR](04_ASSERTION_ERROR.md) that `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

What other things can we compare with `None` to learn more about what it is or is not

### <span style="color:red">**RED**</span>: make a failing test

add a new test to compare `None` with booleans
```python
    def test_is_none_a_boolean(self):
        self.assertIsNone(True)
        self.assertIsNone(False)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

update `test_is_none_a_boolean` to make the tests pass
```python
        self.assertIsNotNone(True)
        self.assertIsNotNone(False)
```
we are reminded that
- `False` is not `None`
- `True` is not `None`
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

booleans are represented by the keyword `bool` in python so we can do an instance test using another `unittest.TestCase` method that checks if an `object` is an instance of a `class`. We cover classes in [CLASSES](CLASSES.md)

### <span style="color:red">**RED**</span>: make a failing test

update `test_is_none_a_boolean` with `self.assertIsInstance`
```python
    self.assertIsInstance(None, bool)
```
the terminal updates to show
```python
AssertionError: None is not an instance of <class 'bool'>
```
because `None` is not an instance of an integer

### <span style="color:green">**GREEN**</span>: make it pass

update `test_is_none_a_boolean` to make the test pass
```python
        self.assertNotIsInstance(None, bool)
```
We can summarize what we know about `None` so far
- `None` is not a boolean
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

- What about other values in python?
- Is `None` equal to any `int`, `float`, `string`, `tuple`, `list`, `set` or `dict`?
Let's find out

### <span style="color:red">**RED**</span>: make a failing test

add a new test to compare `None` with `int`
```python
    def test_is_none_an_integer(self):
        self.assertIsNone(-1)
        self.assertIsNone(0)
        self.assertIsNone(1)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

update `test_is_none_an_integer` to make it pass
```python
        self.assertIsNotNone(-1)
        self.assertIsNotNone(0)
        self.assertIsNotNone(1)
```

### <span style="color:orange">**REFACTOR**</span>: make it better

integers are represented by the keyword `int` in python so we can do an instance test using another `unittest.TestCase` method that checks if an `object` is an instance of a `class`. We cover classes in [CLASSES](CLASSES.md)

### <span style="color:red">**RED**</span>: make a failing test

update `test_is_none_an_integer` with `self.assertIsInstance`
```python
    self.assertIsInstance(None, int)
```
the terminal updates to show
```python
AssertionError: None is not an instance of <class 'int'>
```
because `None` is not an instance of an integer

### <span style="color:green">**GREEN**</span>: make it pass

update `test_is_none_an_integer` to make the test pass
```python
        self.assertNotIsInstance(None, int)
```
So far we know that in python
- `None` is not an integer
- `None` is not a boolean
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's add a test for `strings`

### <span style="color:red">**RED**</span>: make a failing test

update `test_data_structures.py`
```python
    def test_is_none_a_string(self):
        self.assertIsNone('')
        self.assertIsNone("text")
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

update `test_is_none_a_string` to make it pass

```python
        self.assertIsNotNone('')
        self.assertIsNotNone("text")
```

### <span style="color:orange">**REFACTOR**</span>: make it better

`strings` are represented by the `str` class keyword in python. Let's add a test that checks if `None` is an instance of the `string` class

### <span style="color:red">**RED**</span>: make a failing test

update `test_is_none_a_string` and the terminal updates to show a failing test
```python
        self.assertIsInstance(None, str)
```

### <span style="color:green">**GREEN**</span>: make it pass

update the test to make it pass
```python
        self.assertNotIsInstance(None, str)
```
Updating our knowledge of `None`, we know that
- `None` is not a string
- `None` is not an integer
- `None` is not a boolean
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

Is `None` a `tuple`?

### <span style="color:red">**RED**</span>: make a failing test

add a new test to `test_data_structures.py`
```python
    def test_is_none_a_tuple(self):
        self.assertIsNone(())
        self.assertIsNone((1, 2, 3, 'n'))
        self.assertIsInstance(None, tuple)
```
the terminal updates to show an `AssertionError`
```python
AssertionError: () is not None
```
- `()` is how `tuples` are represented in python
- Do you want to [read more about tuples](https://docs.python.org/3/library/stdtypes.html?highlight=tuple#tuple)

### <span style="color:green">**GREEN**</span>: make it pass

- update `test_is_none_a_tuple`
    ```python
        self.assertIsNotNone(())
    ```
    the terminal updates to show
    ```python
    AssertionError: (1, 2, 3, 'n') is not None
    ```
    because the `tuple` that contains the four elements `1, 2, 3, 'n'` is not `None`
- update `test_is_none_a_tuple`
    ```python
        self.assertIsNotNone((1, 2, 3, 'n'))
    ```
    the terminal updates to show
    ```python
    AssertionError: None is not an instance of <class 'tuple'>
    ```
- update the test to make it pass
    ```python
        self.assertNotIsInstance(None, tuple)
    ```
- we now know that in python
    - `None` is not a `tuple`
    - `None` is not a `string`
    - `None` is not an `integer`
    - `None` is not a `boolean`
    - `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

Based on what we have seen so far, is it safe to assume that `None` is only `None` and is not any other data structure?
Let's find out if this assumption is true.

Is `None` a list | array?

### <span style="color:red">**RED**</span>: make a failing test

add a new test
```python
    def test_is_none_a_list(self):
        self.assertIsNone([])
        self.assertIsNone([1, 2, 3, "n"])
        self.assertIsInstance(None, list)
```
the terminal updates to show an `AssertionError`
```python
AssertionError: [] is not None
```
- `[]` is how `lists` are represented in python
- what is the difference between a `list` and a `tuple` other than `[]` vs `()`?
- Do you want to [read more about lists](https://docs.python.org/3/library/stdtypes.html?highlight=tuple#list)

### <span style="color:green">**GREEN**</span>: make it pass

We've done this dance a few times now so we can update `test_is_none_a_list` to make it pass. With the passing tests our knowledge of `None` is updated to
- `None` is not a `list`
- `None` is not a `tuple`
- `None` is not a `string`
- `None` is not an `integer`
- `None` is not a `boolean`
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

Is `None` a `set`?

### <span style="color:red">**RED**</span>: make a failing test

add a new test
```python
    def test_is_none_a_set(self):
        self.assertIsNone({})
        self.assertIsNone({1, 2, 3, "n"})
        self.assertIsInstance(None, set)
```
the terminal updates to show an `AssertionError`
```python
AssertionError: {} is not None
```
- `{}` is how `sets` are represented in python
- Do you want to [read more about sets](https://docs.python.org/3/tutorial/datastructures.html?highlight=sets#sets)

### <span style="color:green">**GREEN**</span>: make it pass

update the tests to make them pass and we can update our knowledge of `None` to state that
- `None` is not a `set`
- `None` is not a `list`
- `None` is not a `tuple`
- `None` is not a `string`
- `None` is not an `integer`
- `None` is not a `boolean`
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

Is `None` a `dictionary | mapping`?

### <span style="color:red">**RED**</span>: make a failing test

add a new test
```python
    def test_is_none_a_dictionary(self):
        self.assertIsNone(dict())
        self.assertIsNone({
            "a": 1,
            "b": 2,
            "c":  3,
            "n": "n"
        })
        self.assertIsInstance(None, dict)
```
the terminal updates to show an `AssertionError`
```python
AssertionError: {} is not None
```
- `dict()` is how we create an empty `dictionary`
- `{}` is how `dictionaries` are represented in python. Wait a minute? What's the difference between a `set` and a `dictionary`?
- There are more tests on `dictionaries` in [DATA_STRUCTURES_DICTIONARIES](13_DATA_STRUCTURES_DICTIONARIES.md)
- Do you want to [read more about dictionaries](https://docs.python.org/3/tutorial/datastructures.html?highlight=sets#dictionaries)

### <span style="color:green">**GREEN**</span>: make it pass

update the tests to make them pass and we can update our knowledge of `None` to state that
- `None` is not a `dictionary`
- `None` is not a `set`
- `None` is not a `list`
- `None` is not a `tuple`
- `None` is not a `string`
- `None` is not an `integer`
- `None` is not a `boolean`
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

We just learned about `None`, which also introduced us to all the `objects` that it is not. Let's do the same with the first `object` we encountered `False`. What is `False` in python?

### <span style="color:red">**RED**</span>: make a failing test

update `test_data_structures.py` with a new test
```python
    def test_what_is_false(self):
        self.assertTrue(None)
        self.assertTrue(False)
        self.assertTrue(0)
        self.assertTrue("")
        self.assertTrue(())
        self.assertTrue([])
        self.assertTrue({})
        self.assertTrue(dict())
        self.assertNotIsInstance(False, bool)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

- change all the `self.assertTrue` statements in `test_what_is_false` to `self.assertFalse` and we have one failing test left.
- update `self.assertNotIsInstance` to `self.assertIsInstance` and all the tests pass
- we now know that in python
    - `False` is a `boolean`
    - `dict()` is `False`
    - `{}` is `False`
    - `[]` is `False`
    - `()` is `False`
    - `""` is `False`
    - `0` is `False`
    - `None` is `False`
    - `None` is not a `dictionary`
    - `None` is not a `set`
    - `None` is not a `list`
    - `None` is not a `tuple`
    - `None` is not a `string`
    - `None` is not an `integer`
    - `None` is not a `boolean`
    - `None` is `None`

we can sum this up as, in python
- `False` is a `boolean`
- empty things including `0` and `None` are `False`
- `None` is `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

What is `True` in python?

### <span style="color:red">**RED**</span>: make a failing test

update `test_data_structures.py` with a new test
```python
    def test_what_is_true(self):
        self.assertFalse(True)
        self.assertFalse(1)
        self.assertFalse(-1)
        self.assertFalse("text")
        self.assertFalse((1, 2, 3, "n"))
        self.assertFalse([1, 2, 3, 'n'])
        self.assertFalse({1, 2, 3, "n"})
        self.assertFalse({
            "a": 1,
            "b": 2,
            "c":  3,
            "n": "n"
        })
        self.assertNotIsInstance(True, bool)
```
the terminal updates to show an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

- change all the `self.assertFalse` statements in `test_what_is_true` to `self.assertTrue` and we have one failing test left.
- update `self.assertNotIsInstance` to `self.assertIsInstance` and all the tests pass
- we can sum up our current knowledge of python thus
    - any value except `0` and `None` is `True`
    - empty things including `0` and `None` are `False`
    - `False` is a `boolean`
    - `True` is a `boolean`
    - `None` is `None`

***HOORAY***

You have built up your knowledge of python, you now know
- Exceptions
- Exception Handling
- Data Structures
    - None
    - boolean
    - int
    - float
    - tuple
    - list
    - dictionary

Take a moment to celebrate