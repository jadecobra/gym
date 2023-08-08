# How to solve the TypeError in Python

This tutorial will step through solving a `TypeError` in Python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## TypeError

A TypeError can be raised when a function is called with the wrong number of inputs.
This means the defined signature of the function was not used when the function was called.

What is a function signature?
What does it mean to call a function?

## How to solve the TypeError in functions

### <span style="color:red">**RED**</span>: Write a failing test

- Open a new file in the editor and save it as `tests/test_type_error.py` in the `tests` folder you created in [Setup Test Driven Development Project](./TDD_SETUP.md) and type the following in the file

    ```python
    import unittest
    import functions


    class TestTypeErrors(unittest.TestCase):
        def test_function_signatures_solve_type_errors(self):
            self.assertIsNone(functions.function_a("a"))
    ```
    the terminal updates to show
    ```shell
        import functions
    E   ModuleNotFoundError: No module named 'functions'
    ```
- Ah, a `ModuleNotFoundError`, We have a lot of practice solving this error from [00_TDD_MODULE_NOT_FOUND_ERROR](./00_TDD_MODULE_NOT_FOUND_ERROR.md). Let's create a file named `functions.py` and the terminal updates to show
    ```shell
    >       self.assertIsNone(functions.function_a("a"))
    E       AttributeError: module 'functions' has no attribute 'function_a'
    ```
- We also have some practice with `AttributeError` from [01_TDD_ATTRIBUTE_ERROR](./01_TDD_ATTRIBUTE_ERROR.md). Add this line `functions.py`
    ```python
    function_a = None
    ```
    the terminal updates to show
    ```shell
    >       self.assertIsNone(functions.function_a("a"))
    E       TypeError: 'NoneType' object is not callable
    ```
    A reminder of our first encounter with `TypeError` from [How to solve the AttributeError by defining a Function](./01_TDD_ATTRIBUTE_ERROR.md)
- We solve this `TypeError` by definining a `callable`, in this case a function. Update `functions.py`
    ```python
    def function_a():
        return None
    ```
    the terminal updates to show
    ```shell
    >       self.assertIsNone(functions.function_a("a"))
    E       TypeError: function_a() takes 0 positional arguments but 1 was given
    ```
    Another `TypeError` but with a message we have not seen before. Reading the error from the bottom up
    - `function_a() takes 0 positional arguments but 1 was given` explains that there was an expectation which was not met in how the function is called. In order words the call violates the signature defined.
    - `self.assertIsNone(functions.function_a("a"))` the offending line. in this line we are checking if this call `functions.function_a("a")` is equal to `None`
    - `functions.function_a("a")` is the call. We can think of it like an address
        - `functions` refers to `functions.py` which is a python module
        - `function_a` refers to `function_a` defined in `functions.py`
        - `()` is how a function is called after it is defined
        - `"a"` is the data/parameter/argument/value that is passed into `function_a`
        Imagine you have a telephone, it has a call function but to make a call you must provide a number then hit dial.
        - `call` is like `function_a`
        - the number you provide is like `"a"` and hitting dial is like `()`
        We will practice this some more in [TDD_FUNCTIONS](./TDD_FUNCTIONS.md)

### <span style="color:green">**GREEN**</span>: Make it Pass

Update `function_a` in `functions.py`
```python
def function_a(data):
    return None
```
the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span> - make it better

There's not much to do here but add more tests for practice.

- add a new test to `test_function_signatures_solve_type_errors` in `test_type_error.py`
    ```python
    self.assertIsNone(functions.function_b("a", "b"))
    ```
    the terminal updates to show
    ```shell
    E       AttributeError: module 'functions' has no attribute 'function_b'
    ```
    update `functions.py`
    ```python
    function_b = None
    ```
    the terminal updates to show
    ```shell
    E       TypeError: 'NoneType' object is not callable
    ```
    change `function_b` to a function, update `function.py`
    ```python
    def function_b():
        return None
    ```
    the terminal updates to show
    ```shell
    >       self.assertIsNone(functions.function_b("a", "b"))
    E       TypeError: function_b() takes 0 positional arguments but 2 were given
    ```
    the offending line `functions.function_b("a", "b")` called `function_b` with 2 parameters but the definition has the function taking no parameters.
- update `function_b` in `functions.py`
    ```python
    def function_b(parameter_1, parameter_2):
        return None
    ```
    the terminal updates to show all tests pass.

***EXTRA***
- What's another solution to the above test?
- How can we define a function that takes in any number of parameters? see [TDD_FUNCTIONS](./TDD_FUNCTIONS.md)