# How to create a calculator using Test Driven Development

This tutorial will step through creating a calculator using Test Driven Development

Here's the Test Driven Development mantra -
    <span style="color:red">**RED**</span> <span style="color:green">**GREEN**</span> <span style="color:orange">**REFACTOR**</span>
- <span style="color:red">**RED**</span> - write a failing test
- <span style="color:green">**GREEN**</span> - make it pass
- <span style="color:orange">**REFACTOR**</span> - rewrite the solution to make it better

## Prerequisites

- [python](https://www.python.org/downloads/)
- an Interactive Development Environment(IDE) - using VSCode, there are other options
    - [VSCode in a Browser](http://vscode.dev)
    - [Download VSCode](https://code.visualstudio.com/download)

## Setup

### Setup File Structure

in a terminal type the following to setup the directory structure

**NOTE** If you are on a Windows machine, replace `touch` in the example below with `New-Item`
```shell
mkdir -p calculator/tests
cd calculator
touch calculator.py
touch tests/__init__.py
touch tests/test_calculator.py
code .
```

- The name of the project is calculator
- Tests are stored in the `tests` folder to separate them from the actual source code
- The `tests` folder contains `__init__.py` to tell python that this is a module
- The actual test file is called `test_calculator.py`
- The module we are creating is called `calculator.py`. A python module is any file that ends in `.py`

### <span style="color:red">**RED**</span>: Write a failing test

Open up `calculator/tests/test_calculator.py` in your IDE and type the following

```python
import unittest


class TestCalculator(unittest.TestCase):

    def test_failure(self):
        self.assertFalse(True)
```

- what is `unittest`? it is a module|library that comes with python for testing code
- what is the `TestCalculator` class? it is a container for the tests we are about to write
- what is `unittest.TestCase`? a class defined in the `unitest` library which contains a bunch of `methods|functions` for testing code that `TestCalculator` inherits so I do not have to rewrite them
- what is inheritance? a simple way to think of it is that `TestCalculator` is a child of `unittest.TestCase`
- what is `def test_failure`? it is the definition of a test function to test the system being built?
- what is `self`? self refers to the `TestCalculator` class. To access things within the class `self` is used, it avoids having to say `TestCalculator.assertFalse(True)`
- what is `self.assertFalse(True)`? an assert statement that is a substitute for `assert False == True` which is like asking the question `is False equal to True?`

to test the code, write the following in the terminal

```shell
python3 -m unittest -f
```

you should get the following result
```python
F
======================================================================
FAIL: test_failure (tests.TestCalculator.test_failure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/<PATH_TO_CALCULATOR>/calculator/tests/test_calculator.py", line 7, in test_failure
    self.assertFalse(True)
AssertionError: True is not false

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

<span style="color:red">*CONGRATULATIONS!*</span> You have written your first test.

This iterative process is what we are following. We are currently <span style="color:red">**RED**</span>
The error provides important information about the code. Reading from the bottom
- `FAILED (failures=1)` The test failed - <span style="color:red">**RED**</span>
- `Ran 1 test in 0.000s` python ran the 1 test written in 0.000s
- `AssertionError: True is not false` The error is an `AssertionError`. This errors are raised by python when an assert statement is false. It further gives the False Assertion `True is not false`. It is good practice to keep track of error types aka Exceptions, they will help you be a better troubleshooter.
- `self.assertFalse(True)` the line of code that caused the failure
- `File "/<PATH_TO_CALCULATOR>/calculator/tests/test_calculator.py", line 7, in test_failure` where in the file the error occurred - line 7 in the `test_failure` function in the `test_calculator.py` file. Clicking on this line will place your cursor at the position in the IDE
- `Traceback (most recent call last):` all the information returned by python is the traceback, showing the most recent call python made last.
- `FAIL: test_failure (tests.TestCalculator.test_failure)` a header giving information about the test
    - `tests.TestCalculator.test_failure` is the location of the failing test
      - `tests` - tests folder
      - `TestCalculator` - the class defined on line 4
      - `test_failure` - the function defined on line 6
- `F` indicating a failure

### <span style="color:green">**GREEN**</span>: Make it Pass

change line 7 to make the test pass. Which do you think is a better solution?
- `self.assertTrue(True)` or
- `self.assertFalse(True)`

run the test again from the terminal
```shell
python3 -m unittest
```
response
```shell
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

<span style="color:green">*CONGRATULATIONS!*</span> You have a passing test. <span style="color:green">**GREEN**</span>