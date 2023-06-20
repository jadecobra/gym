# How to solve the AttributeError in Python

This tutorial will step through solving an AttributeError in Python using Test Driven Development

Here's the Test Driven Development mantra -
    <span style="color:red">**RED**</span> <span style="color:green">**GREEN**</span> <span style="color:orange">**REFACTOR**</span>
- <span style="color:red">**RED**</span> - write a failing test
- <span style="color:green">**GREEN**</span> - make it pass
- <span style="color:orange">**REFACTOR**</span> - make it better

## Prerequisites

- [download and install python](https://www.python.org/downloads/)
- an Interactive Development Environment(IDE) - Here are a few options
    - [VSCode in a Browser](http://vscode.dev)
    - [Download VSCode](https://code.visualstudio.com/download)
    - [Download PyCharm](https://www.jetbrains.com/pycharm/download/#section=mac)
    - [Download Sublime](https://www.sublimetext.com)
    - [Other IDE options](https://wiki.python.org/moin/IntegratedDevelopmentEnvironments)

## Setup

> ***Are you on a Windows machine?***
> - replace `touch` in the example below with `New-Item`
> - replace `python3` in the examples with `python`

---

### Setup File Structure

in a terminal type the following to setup the directory structure

```shell
mkdir -p python_tdd/tests
cd python_tdd
touch tests/__init__.py
touch tests/test_attribute_error.py
```

### <span style="color:red">**RED**</span>: Write a failing test

- Open up `python_tdd/tests/test_attribute_error.py` in your IDE and type the following
    ```python
    import unittest


    class TestAttributeError(unittest.TestCase):

        def test_failure(self):
            self.assertFalse(True)
    ```
- `import unittest` imports an existing module from the python standard library that is used for testing. [read more](https://docs.python.org/3/library/unittest.html?highlight=unittest#module-unittest)
- what is `unittest`? it is a module|library that comes with python for testing code
- what is the `TestAttributeError` class? it is a container for the tests we are about to write
- what is `unittest.TestCase`? a class defined in the `unitest` library which contains a bunch of `methods|functions` for testing code that `TestAttributeError` inherits so I do not have to rewrite them
- what is inheritance? a simple way to think of it is that `TestAttributeError` is a child of `unittest.TestAttributeError`
- what is `def test_failure`? it is the definition of a test function to test the system being built?
- what is `self`? self refers to the `TestAttributeError` class. To access things within the `TestCalculator` class `self` is used. It avoids having to say `TestAttributeError.assertFalse(True)`
- what is `self.assertFalse(True)`? an assert statement that is a substitute for `assert False == True` which is similar to asking the question `is False equal to True?`
- to test the code, write the following in the terminal
    ```shell
    python3 -m unittest
    ```
    you should get the following result
    ```python
    F
    ======================================================
    FAIL: test_failure (tests.TestAttributeError.test_failure)
    ------------------------------------------------------
    Traceback (most recent call last):
    File "/<PATH_TO_PROJECT>/python_tdd/tests/test_attribute_error.py", line 7, in test_failure
        self.assertFalse(True)
    AssertionError: True is not false

    ------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (failures=1)
    ```

<span style="color:red">*CONGRATULATIONS!*</span> You have written your first test.

We follow the iterative process of <span style="color:red">**RED**</span> <span style="color:green">**GREEN**</span> <span style="color:orange">**REFACTOR**</span>. We are currently <span style="color:red">**RED**</span>
The error provides important information about the code. Reading from the bottom
- `FAILED (failures=1)` The test failed - <span style="color:red">**RED**</span>
- `Ran 1 test in 0.000s` python ran the 1 test written in 0.000s
- `AssertionError: True is not false` The error is an [AssertionError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#AssertionError). This is raised by python when an assert statement fails
- It further gives the False Assertion `True is not false`.
- Keep a running tab of Errors aka Exceptions seen as you go through this exercise, they will help you be a better troubleshooter.
    ```python
    import unittest


    class TestAttributeError(unittest.TestCase):

        def test_failure(self):
            self.assertFalse(True)

    # Exceptions Encountered
    # AssertionError
    ```
- `self.assertFalse(True)` the line of code that caused the failure
- `File "/<PATH_TO_PROJECT>/python_tdd/tests/test_attribute_error.py", line 7, in test_failure` where in the file the error occurred - line 7 in the `test_failure` function in the `test_attribute_error.py` file. Clicking on this line will place your cursor at the position in the IDE
- `Traceback (most recent call last):` all the information returned by python is the traceback, showing the most recent call python made last.
- `FAIL: test_failure (tests.TestAttributeError.test_failure)` a header giving information about the test
    - `tests.TestAttributeError.test_failure` is the location of the failing test
      - `tests` - tests folder
      - `TestAttributeError` - the class defined on line 4
      - `test_failure` - the function defined on line 6
- `F` indicates a failure

---

### <span style="color:green">**GREEN**</span>: Make it Pass

change line 7 to make the test pass. Which do you think is a better solution?
`self.assertTrue(True)` or `self.assertFalse(True)`

run the test again from the terminal
```shell
python3 -m unittest
```
terminal response
```shell
.
------------------------------------------------------
Ran 1 test in 0.000s

OK
```

<span style="color:green">*CONGRATULATIONS!*</span> You have a passing test. We are <span style="color:green">**GREEN**</span>

---

### <span style="color:orange">**REFACTOR**</span> - Make it Better

One way to make code better is to use the
- [Abstraction Principle](https://en.wikipedia.org/wiki/Abstraction_principle_(computer_programming))
- [Do Not Repeat Yourself (DRY)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

So far there's not much to improve on what has been written but there has been duplication.
- we ran `python3 -m unittest` to see the test fail
- we ran `python3 -m unittest` to see the test pass
- we run `python3 -m unittest` to make sure our improvements do not break previous tests

This means for every test we introduce we have to run that command 3 times.
How can we avoid this repetition and focus on tests and solutions?

---
