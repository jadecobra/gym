# How to solve the TypeError in python

We will step through solving a `TypeError` in python using Test Driven Development

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## TypeError

A TypeError can be raised when a function is called with the wrong number of inputs.
This means the defined signature of the function was not used when the function was called.

What is a function signature?
What does it mean to call a function?

## How to solve the TypeError in functions

### <span style="color:red">**RED**</span>: make it fail

- Open a new file in the editor and save it as `tests/test_type_error.py` in the `tests` folder you created in [Setup a Test Driven Development Environment](./TDD_SETUP.md) and type the following in the file

    ```python
    import unittest
    import functions


    class TestTypeErrors(unittest.TestCase):
        def test_function_signatures_solve_type_errors(self):
            self.assertIsNone(functions.function_a("a"))
    ```
    the terminal updates to show
    ```python
        import functions
    E   ModuleNotFoundError: No module named 'functions'
    ```
- Ah, a `ModuleNotFoundError`, We have a lot of practice solving this error from [00_TDD_MODULE_NOT_FOUND_ERROR](./00_TDD_MODULE_NOT_FOUND_ERROR.md). Let's create a file named `functions.py` and the terminal updates to show
    ```python
    >       self.assertIsNone(functions.function_a("a"))
    E       AttributeError: module 'functions' has no attribute 'function_a'
    ```
- We also have some practice with `AttributeError` from [01_TDD_ATTRIBUTE_ERROR](./01_TDD_ATTRIBUTE_ERROR.md). Add this line `functions.py`
    ```python
    function_a = None
    ```
    the terminal updates to show
    ```python
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
    ```python
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

### <span style="color:green">**GREEN**</span>: make it pass

Update `function_a` in `functions.py`
```python
def function_a(data):
    return None
```
the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

There's not much to do here but add more tests for practice.

- add a new test to `test_function_signatures_solve_type_errors` in `test_type_error.py`
    ```python
    self.assertIsNone(functions.function_b("a", "b"))
    ```
    the terminal updates to show
    ```python
    AttributeError: module 'functions' has no attribute 'function_b'
    ```
    update `functions.py`
    ```python
    function_b = None
    ```
    the terminal updates to show
    ```python
    TypeError: 'NoneType' object is not callable
    ```
    change `function_b` to a function, update `function.py`
    ```python
    def function_b():
        return None
    ```
    the terminal updates to show
    ```python
    >       self.assertIsNone(functions.function_b("a", "b"))
    E       TypeError: function_b() takes 0 positional arguments but 2 were given
    ```
    the offending line `functions.function_b("a", "b")` called `function_b` with 2 parameters but the definition has the function taking no parameters.
- update `function_b` in `functions.py`
    ```python
    def function_b(positional_argument_1):
        return None
    ```
    the terminal updates to show
    ```python
    TypeError: function_b() takes 1 positional argument but 2 were given
    ```
    ah, our previous definition only allowed for 0 positional arguments, now it allows for 1 positional argument but we are still calling with 2 positional arguments.

    update `function_b` in `functions.py` to take in 2 positional arguments
    ```python
    def function_b(positional_argument_1, positional_argument_2):
        return None
    ```
    the terminal updates to show all tests pass.

***EXTRA***
- What's another solution to the above test?
- How can we define a function that takes in any number of parameters? see [TDD_FUNCTIONS](./TDD_FUNCTIONS.md)

### Let's add more tests

#### <span style="color:red">**RED**</span>: make it fail

update `TestTypeErrors` in `test_type_error.py` to add more tests
```python
self.assertIsNone(functions.function_c("a", "b", "c"))
```
the terminal updates to show
```python
AttributeError: module 'functions' has no attribute 'function_c'
```

#### <span style="color:green">**GREEN**</span>: make it pass

update `functions.py`
```python
function_c = None
```
the terminal updates to show
```python
TypeError: 'NoneType' object is not callable
```
update `functions.py` to make `function_c` a function
```python
def function_c():
    return None
```
the terminal updates to show
```python
TypeError: function_c() takes 0 positional arguments but 3 were given
```
update `function_c` in `functions.py` to take in an argument
```python
def function_c(arg1):
    return None
```
the terminal updates to show
```python
TypeError: function_c() takes 1 positional argument but 3 were given
```
update `function_c` in `functions.py` to take in another argument
```python
def function_c(arg1, arg2):
    return None
```
the terminal updates to show
```python
TypeError: function_c() takes 2 positional arguments but 3 were given
```
update `function_c` in `functions.py` to take in one more argument
```python
def function_c(arg1, arg2, arg3):
    return None
```
and the terminal updates to show all tests pass

#### <span style="color:orange">**REFACTOR**</span>: make it better

are you bored yet? let's add one more test

update `TestTypeErrors` in `test_type_error.py`
```python
    self.assertIsNone(functions.function_d("a", "b", "c", "d"))
```
the terminal updates to show
```python
AttributeError: module 'functions' has no attribute 'function_d'
```
update `functions.py`
```python
function_d = None
```
the terminal updates to show
```python
 TypeError: 'NoneType' object is not callable
```
update `function_d` in `functions.py`
```python
def function_d():
    return None
```
the terminal updates to show
```
TypeError: function_d() takes 0 positional arguments but 4 were given
```
let's try our solution for the previous test. update the signature of `function_d` in `functions.py`
```python
def function_d(arg1, arg2, arg3):
    return None
```
the terminal updates to show
```python
TypeError: function_d() takes 3 positional arguments but 4 were given
```
update `function_d` in `functions.py` to take 4 arguments
```python
def function_d(arg1, arg2, arg3, arg4):
    return None
```
the terminal updates to show all tests pass...but wait! there's more. We can make this better. There's another solution to the above test. What if we can define a function that takes in any number of parameters, is there a signature that allows a function to take 1 argument, 4 arguments, or any number of arguments?

YES! There is we can use the `*args` keyword to pass in any number of positional arguments to a function

update `function_d` in `functions.py` with `*args`
```python
def function_d(*args):
    return None
```
the terminal shows all tests as still passing. FANTASTIC!!

Let's test this with `function_a`. update `function_a` in `functions.py` with `*args` and the terminal shows all tests as still passing.

Try this with both `function_c` and `function_d`, all tests still pass.

***LOVELY!!!***
You now know how to solve
- `AssertionError`
- `ModuleNotFoundError`
- `NameError`
- `AttributeError` by defining
    - variables
    - functions
    - classes
    - attributes in classes
    - functions/methods in classes
- `TypeError` by matching function signatures and their calls