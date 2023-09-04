# How to handle Exceptions in python

We will step through handling Exceptions in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Exceptions

Exceptions break execution in a program. When an exception is encountered no further instructions in the program will run.
This is useful because it means there is some violation that should be taken care of for the program to proceed as intended.
It also a pain when it causes the program to exit prematurely. What if we want our program to run regardless of errors?
What if we want our programs to give messages to the user who is not technical and cannot understand Exception messages?

Enter Exception Handling. In programming there is a mechanism for handling exceptions that allows a program to "make a decision" when it encounters an Exception. Enough words, let us write some code

## How to Handle Exceptions

### How to test that an Exception is raised

#### <span style="color:red">**RED**</span>: make it fail

create a file named `test_exception_handling.py` in the `tests` folder and add the following

```python
import unittest
import module


class TestExceptionHandling(unittest.TestCase):

    def test_catching_module_not_found_error_in_tests(self):
        import non_existent_module
```
the terminal updates to show `ModuleNotFoundError`. We know one solution is to create the module, but in this case we want to catch/handle the exception in the test as a way to prove in the code that a `ModuleNotFoundError` will be raised for this module `non_existent_module` that does not exist

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_catching_module_not_found_error_in_tests`

```python
    def test_catching_module_not_found_error_in_tests(self):
        with self.assertRaises(ModuleNotFoundError):
            import non_existent_module
```

the terminal updates to show passing tests. How does all this work?
- we use the `self.assertRaises` method from `unittest.TestCase` which takes a given exception, in this case `ModuleNotFoundError` and checks if that error is raised by the statements given in the context
- `with` - creates the context in which we are testing the exception is created.
    - Do you want to [read more about the with statement](https://docs.python.org/3/reference/compound_stmts.html?highlight=statement#the-with-statement)?
    - Do you want to [read more about with statement context managers](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers)?
    - Do you want to [read PEP 343 - The "with" Statement](https://peps.python.org/pep-0343/)?

### <span style="color:orange">**REFACTOR**</span>: make it better

We now know how to catch/handle an exception with `unittest`. What can we do with this?
- How can we test that a program fails in an expected way?
- How can we deliberately create an exception?
- How can we design for failure?

### <span style="color:red">**RED**</span>: make it fail

add a new test to `TestExceptionHandling` in `test_exception_handling.py`

```python
    def test_catching_attribute_errors_in_tests(self):
        module.non_existent_attribute
```
the terminal updates to show `AttrbuteError` because the called attribute `non_existent_attribute` does not exist in `module.py`
```python
E       AttributeError: module 'module' has no attribute 'non_existent_attribute'
```

### <span style="color:green">**GREEN**</span>: make it pass

update `test_catching_attribute_errors_in_tests` with `self.assertRaises`
```python
        with self.assertRaises(AttributeError):
            module.non_existent_attribute
```
the terminal updates to show passing tests. Let's do it again

### <span style="color:red">**RED**</span>: make it fail

update `test_catching_attribute_errors_in_tests`

```python
        module.non_existent_function()
```
the terminal updates to show `AttrbuteError` because the called attribute `non_existent_attribute` does not exist in `module.py`
```python
E       AttributeError: module 'module' has no attribute 'non_existent_function'
```

### <span style="color:green">**GREEN**</span>: make it pass

add `self.assertRaises` and indent the failing line
```python
        with self.assertRaises(AttributeError):
            module.non_existent_function()
```
the terminal updates to show passing tests

### <span style="color:red">**RED**</span>: make it fail

let's add another failing line to `test_catching_attribute_errors_in_tests`

```python
        module.NonExistentClass()
```
the terminal updates to show
```python
E       AttributeError: module 'module' has no attribute 'NonExistentClass'
```


### <span style="color:green">**GREEN**</span>: make it pass

add `self.assertRaises` to make it pass
```python
        with self.assertRaises(AttributeError):
            module.NonExistentClass()
```
the terminal shows passing tests

### <span style="color:red">**RED**</span>: make it fail

update `test_catching_attribute_errors_in_tests` with the following
```python
        module.Class.non_existent_attribute
```
the terminal updates to show
```python
E       AttributeError: type object 'Class' has no attribute 'non_existent_attribute'
```

### <span style="color:green">**GREEN**</span>: make it pass

add `self.assertRaises` to catch the error
```python
        with self.assertRaises(AttributeError):
            module.Class.non_existent_attribute
```
the terminal updates to show passing tests

### <span style="color:red">**RED**</span>: make it fail

let's add another attribute error, update `test_catching_attribute_errors_in_tests`
```python
        module.Class.non_existent_method()
```
the terminal updates to show
```python
E       AttributeError: type object 'Class' has no attribute 'non_existent_method'
```
### <span style="color:green">**GREEN**</span>: make it pass

add `self.assertRaises` to make it pass
```python
        with self.assertRaises(AttributeError):
            module.Class.non_existent_method()
```
the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

We just wrote the same context manager 5 times, this is a good candidate for a rewrite. Let's remove the duplication. Update `test_catching_attribute_errors_in_tests`
```python
        with self.assertRaises(AttributeError):
            module.non_existent_attribute
            module.non_existent_function()
            module.NonExistentClass()
            module.Class.non_existent_attribute
            module.Class.non_existent_method()
```
the terminal shows our tests are still passing

### <span style="color:red">**RED**</span>: make it fail

Let's try another exception. add a new test to `test_exception_handling.py`
```python
    def test_catching_zero_dvision_error_in_tests(self):
        1 / 0
```
the terminal updates to show
```python
E       ZeroDivisionError: division by zero
```

In [TDD_CALCULATOR](./TDD_CALCULATOR.md), we built a calculator and ran into issues when dividing by zero. In Mathematics, dividing by zero is undefined and in python it raises a `ZeroDivisionError`. To solve that problem we modified the test to do something else if the divisor was ever 0. Let's take a different approach.
- What if we want the program to return a message instead of ending execution of the program abruptly?
- What if we want to assert that dividing by zero causes an error but the error it causes does not end our tests?

### <span style="color:green">**GREEN**</span>: make it pass

add `self.assertRaises` to make the test pass
```python
        with self.assertRaises(ZeroDivisionError):
            1 / 0
```
the terminal updates to show passing tests

## How to Handle Exceptions in programs

### <span style="color:red">**RED**</span>: make it fail
we will deliberately create an exception in our code and then handle it. update `test_exception_handling.py` with a new test.
```python
    def test_catching_exceptions(self):
        exceptions.raise_exception_error()
```
the terminal updates to show a `NameError`

### <span style="color:green">**GREEN**</span>: make it pass
- update the import section with a new import
    ```python
    import unittest
    import module
    import exceptions
    ```
    the terminal updates to show a `ModuleNotFoundError`
- create a file named `exceptions.py` in the `project_name` folder, and the terminal updates to show an `AttributeError`
- update `exceptions.py` and the terminal updates to show a `NameError` since we have not defined `raises_exception_error`
    ```python
    raises_exception_error
    ```
- define `raises_exception_error` and the terminal updates to show a `TypeError`
    ```python
    raises_exception_error = None
    ```
- redefine `raises_exception_error` as a function and the terminal updates to show passing tests
    ```python
    def raises_exception_error():
        return None
    ```
- let's update the function to raise an Exception
    ```python
    def raises_exception_error():
        raise Exception
    ```
    the terminal updates to show
    ```python
    E       Exception
    ```
- update `test_catching_exceptions` in `test_exception_handling.py` with `self.assertRaises`
    ```python
        with self.assertRaises(Exception):
            exceptions.raises_exception_error()
    ```
    the terminal shows passing tests.

***CONGRATULATIONS**
You now know how to deliberately create an exception.

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's add exception handling to our program so it does not end when it encounters the exceptions we handle

#### <span style="color:red">**RED**</span>: make it fail

add a new test to `test_exception_handling`
```python
    def test_catching_things_that_fail(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.raises_exception_error),
            'failed'
        )
```
the terminal updates to show an `AttributeError`

#### <span style="color:green">**GREEN**</span>: make it pass
- update `exceptions.py` with a new name and the terminal updates to show `NameError`
    ```python
    exception_handler
    ```
- define `exception_handler` and the terminal updates to show `TypeError`
    ```python
    exception_handler = None
    ```
- redefine `exception_handler` and the terminal updates to show `TypeError`
    ```python
    def exception_handler():
        return None
    ```
- update the signature for `exception_handler` to accept a positional argument
    ```python
    def exception_handler(argument):
        return None
    ```
    the terminal updates to show
    ```python
    E       AssertionError: None != 'failed'
    ```
    because the result of calling `exceptions.exception_handler(exceptions.raises_exception_error)` is currently `None` which is not equal to `failed`
- update `exception_handler` to return `failed` and the terminal updates to show passing tests
    ```python
    def exception_handler(argument):
        return 'failed'
    ```

#### <span style="color:red">**RED**</span>: make it fail

add a new test to `test_exception_handling`
```python
    def test_catching_things_that_succeed(self):
        self.assertEqual(
            exceptions.exception_handler(exceptions.succeeding_function),
            'succeeded'
        )
```
the terminal updates to show an `AttributeError`

#### <span style="color:green">**GREEN**</span>: make it pass

- update `exceptions.py` with `succeeding_function` and the terminal updates to show a `NameError`
    ```python
    succeeding_function
    ```
- define `succeeding_function`
    ```python
    succeeding_function = None
    ```
    and the terminal updates to show
    ```
    E       AssertionError: 'failed' != 'succeeded'
    ```
    because the value of `exceptions.exception_handler(exceptions.succeeding_function)` is `failed` which is not equal to `succeeded`
- How can we make the same function return different values based on the input it receives? In this case, based on the exceptions that occur within the function. update `exception_handler` in `exceptions.py` to call a function when it is passed in
    ```python
    def exception_handler(function):
        return function()
    ```
    the terminal updates to show a `TypeError` because `succeeding_function` is not a function
- redefine `succeeding_function` to make it callable
    ```python
    def succeeding_function():
        return None
    ```
    the terminal updates to show
    ```python
    AssertionError: None != 'succeeded'
    ```
    because the result of executing `exceptions.exception_handler(exceptions.succeeding_function)` is `None` which is not equal to `succeeded`
- To catch|handle exceptions we use a `try...except...else` statement. This allows the program to make a decision when it encounters an Exception. Update `exception_handler` in `exceptions.py`
    ```python
    def exception_handler(function):
        try:
            function()
        except Exception:
            return 'failed'
        else:
            return 'succeeded'
    ```
    the terminal updates to show passing tests
- Why does this work? What is a `try...except...else` statement? We can think of it as `try` something and if it raises an `Exception` do this but if the `try` portion succeeds, then do something else. In this case
    - `try` calling `function()`
    - `except Exception` - if `function()` raises an Exception return `failed`
    - `else` - if `function()` does not raise an Exception return `succeeded`
    - do you want to
      - [read more about `try...except...else`?](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement)
      - [read more about exception handling?](https://docs.python.org/3/tutorial/errors.html?highlight=try%20except#handling-exceptions)

### <span style="color:orange">**REFACTOR**</span>: make it better

### <span style="color:red">**RED**</span>: make it fail

update `test_exception_handling.py` and the terminal updates to show an `AttributeErroor`
```python
    def test_finally_always_returns(self):
        self.assertEqual(
            exceptions.always_returns(exceptions.succeeding_function),
            "always_returns_this"
        )
```

### <span style="color:green">**GREEN**</span>: make it pass

- update `exceptions.py` and the terminal updates to show a `NameError`
    ```python
    always_returns
    ```
- define `always_returns` and the terminal updates to show an `AttributeError`
    ```python
    always_returns = None
    ```
- redefine `always_returns` and the terminal updates to show a `TypeError`
    ```python
    def always_returns():
        return None
    ```
- update the signature of `always_returns` to accept a positional argument
    ```python
    def always_returns(function):
        return function()
    ```
    the terminal updates to show
    ```python
    AssertionError: None != 'always_returns_this'
    ```
    because the result of executing `exceptions.always_returns(exceptions.succeeding_function)` is `None` which is not equal to `always_returns_this`
- add exception handling with a `finally` clause
    ```python
    def always_returns(function):
        try:
            function()
        except Exception:
            return 'failed'
        else:
            return 'succeeded'
        finally:
            return 'always_returns_this'
    ```
    the terminal updates to show passing tests. the `finally` clause is always executed regardless of what happens in the `try` block
- let's add one more test to verify that the code in the `finally` block will always execute. update `test_finally_always_returns`
    ```python
        self.assertEqual(
            exceptions.always_returns(exceptions.raises_exception_error),
            'always_returns_this'
        )
    ```
    the terminal shows passing tests

***WELL DONE***
You made it through a lengthy chapter.