# How to create a calculator using Test Driven Development

This tutorial will step through creating a calculator using Test Driven Development

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

### Setup File Structure

in a terminal type the following to setup the directory structure

```shell
mkdir -p calculator/tests
cd calculator
touch calculator.py
touch tests/__init__.py
touch tests/test_calculator.py
code .
```

- the name of the project is `calculator`
- Tests are stored in the `tests` folder to separate them from the actual source code
- The `tests` folder contains `__init__.py` to tell python that this is a module
- The actual test file is called `test_calculator.py`
- The module we are creating is called `calculator.py`
- What is a module? A python module is any file that ends in `.py`

---

### <span style="color:red">**RED**</span>: Write a failing test

- Open up `calculator/tests/test_calculator.py` in your IDE and type the following
    ```python
    import unittest


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertFalse(True)
    ```
- `import unittest` imports an existing module from the python standard library that is used for testing. [read more](https://docs.python.org/3/library/unittest.html?highlight=unittest#module-unittest)
- what is `unittest`? it is a module|library that comes with python for testing code
- what is the `TestCalculator` class? it is a container for the tests we are about to write
- what is `unittest.TestCase`? a class defined in the `unitest` library which contains a bunch of `methods|functions` for testing code that `TestCalculator` inherits so I do not have to rewrite them
- what is inheritance? a simple way to think of it is that `TestCalculator` is a child of `unittest.TestCase`
- what is `def test_failure`? it is the definition of a test function to test the system being built?
- what is `self`? self refers to the `TestCalculator` class. To access things within the `TestCalculator` class `self` is used. It avoids having to say `TestCalculator.assertFalse(True)`
- what is `self.assertFalse(True)`? an assert statement that is a substitute for `assert False == True` which is similar to asking the question `is False equal to True?`
- to test the code, write the following in the terminal
    ```shell
    python3 -m unittest
    ```
    you should get the following result
    ```python
    F
    ======================================================
    FAIL: test_failure (tests.TestCalculator.test_failure)
    ------------------------------------------------------
    Traceback (most recent call last):
    File "/<PATH_TO_CALCULATOR>/calculator/tests/test_calculator.py", line 7, in test_failure
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


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertFalse(True)

    # Exceptions Encountered
    # AssertionError
    ```
- `self.assertFalse(True)` the line of code that caused the failure
- `File "/<PATH_TO_CALCULATOR>/calculator/tests/test_calculator.py", line 7, in test_failure` where in the file the error occurred - line 7 in the `test_failure` function in the `test_calculator.py` file. Clicking on this line will place your cursor at the position in the IDE
- `Traceback (most recent call last):` all the information returned by python is the traceback, showing the most recent call python made last.
- `FAIL: test_failure (tests.TestCalculator.test_failure)` a header giving information about the test
    - `tests.TestCalculator.test_failure` is the location of the failing test
      - `tests` - tests folder
      - `TestCalculator` - the class defined on line 4
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
After the failing test we ran `python3 -m unittest` to see it fail,
After we corrected the test we ran `python3 -m unittest` to see if pass,
If we make an improvement we have to run `python3 -m unittest` to make sure the change does not break functionality.
This means for every test we introduce we have to run that command 3 times.
How can we avoid this repetition and focus on tests and solutions?

---

#### How to Automatically Run Tests

##### Setup a Virtual Environment

> ***Are you on a Windows machine?***
> - replace `python3` in the examples with `python`
> - replace `source .venv/bin/activate` in the example below with `.venv/scripts/activate`

type the following in the terminal
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install pytest-watch
```

You just created a [virtual environment](https://docs.python.org/3/library/venv.html)
- `python3 -m venv .venv` creates a virtual environment named `.venv` you can use any name you want
- `source .venv/bin/activate` or `.venv/scripts/activate` activates the virtual environment
- `pip install -U pip` - upgrades `pip` to the latest version
- what is pip? the [python package manager](https://pypi.org/project/pip/)
- `pip install pytest-watch` installs a python library named `pytest-watch` that will automatically run the tests when a change is made

run the tests by typing `pytest-watch` in the terminal, you should see something similar to
```shell
[TODAYS_DATE] Running: py.test
======================= test session starts==========================
platform <YOUR_OPERATING_SYSTEM> -- Python <YOUR_PYTHON_VERSION>, pytest-<VERSION>, pluggy-<VERSION>
rootdir: <YOUR_PATH>/calculator
collected 1 item

tests/test_calculator.py .                                                                                                    [100%]

======================= 1 passed in 0.00s ============================
```

---

## Add More Tests

Update `test_calculator.py` with a TODO list to keep track of what needs to be done
```python
import unittest


class TestCalculator(unittest.TestCase):

    def test_failure(self):
        self.assertTrue(True)

# TODO
# test importing
# test addition
# test subtraction
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
```

the terminal should respond since a change was made

```shell
=============== 1 passed in 0.01s ===========================

Change detected: tests/test_calculator.py

[TODAYS_DATE] Running: py.test
===================== test session starts ===================
platform <YOUR_OPERATING_SYSTEM> -- Python <YOUR_PYTHON_VERSION>, pytest-<VERSION>, pluggy-<VERSION>
rootdir: <YOUR_PATH>/calculator
collected 1 item

tests/test_calculator.py .                                                                                                    [100%]

==================== 1 passed in 0.00s =====================
```

### Add the import test

```python
import unittest
import calculator


class TestCalculator(unittest.TestCase):

    def test_failure(self):
        self.assertTrue(True)

# TODO
# test importing
# test addition
# test subtraction
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
```

- `import calculator` - imports the calculator module we are writing/testing

### Test Addition

#### <span style="color:red">**RED**</span>: Write a failing test

```python
import unittest
import calculator


class TestCalculator(unittest.TestCase):

    def test_failure(self):
        self.assertTrue(True)

    def test_addition(self):
        self.assertEqual(
            calculator.add(0, 1),
            1
        )

# TODO
# test addition
# test subtraction
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
```

- remove `test import` from the TODO list since it passed and the task is completed
- add `test_addition` to the list of tests
- there's a new method `self.assertEqual` this checks if 2 things are the same it is similar to `assert x == y` or asking `is x equal to y?`
- there are two things passed to the `self.assertEqual` for evaluation
    - calculator.add(0, 1) - when we pass the values 0 and 1 to the addition function
    - 1 - we expect it to return one

    the terminal updates with the following

    ```python
    ...
    collected 2 items

    tests/test_calculator.py F.                                                                                                   [100%]

    =========================== FAILURES =======================
    ______________ TestCalculator.test_addition ________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
    >           calculator.add(0, 1),
                1
            )
    E       AttributeError: module 'calculator' has no attribute 'add'

    tests/test_calculator.py:12: AttributeError
    ============== short test summary info +=======================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - AttributeError: module 'calculator' has no attribute 'add'
    ============ 1 failed, 1 passed in 0.02s ======================
    ```

    What does this mean?
    - The error is an `AttributeError` at line 12 in `test_calculator.py`
    - [AttributeError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#AttributeError) is raised when you try to access an attribute and python cannot find it
    - `calculator.add` is similar to an address. `calculator` refers to `calculator.py` - the python module we wrote at the beginning
    - `add` refers to something in that file that currently does not exist


#### <span style="color:green">**GREEN**</span>: Make it Pass

- open `calculator.py` in your IDE and add this
    ```python
    add = None
    ```

    the terminal will update to show a new Error

    ```python
    ================== FAILURES =============================
    ___________ TestCalculator.test_addition ________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
    >           calculator.add(0, 1),
                1
            )
    E       TypeError: 'NoneType' object is not callable

    tests/test_calculator.py:12: TypeError
    =============== short test summary info ========================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - TypeError: 'NoneType' object is not callable
    ============== 1 failed, 1 passed in 0.03s ======================
    ```

- The `AttributeError` was fixed by declaring a variable `add` in the `calculator` module, even though it is currently defined as the null value `None`
- The new error is [TypeError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#TypeError) occurs when an `object` is used in a way that it was not intended for. The `add` variable is not callable. Let's make it callable

    update `calculator.py` to
    ```python
    def add():
        return None
    ```

    the terminal will update to a different message for the TypeError

    ```python
    ===================== FAILURES ===========================
    ___________ TestCalculator.test_addition _________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
    >           calculator.add(0, 1),
                1
            )
    E       TypeError: add() takes 0 positional arguments but 2 were given

    tests/test_calculator.py:12: TypeError
    ============== short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - TypeError: add() takes 0 positional arguments but 2 were given
    ============= 1 failed, 1 passed in 0.02s ===================
    ```
- This `TypeError` indicates that the current definition of the `add` function takes in no arguments but we provided 2. update the `add` function in `calculator.py` to match the test
    ```
    def add(x, y):
        return None
    ```
    the terminal updates to a new error
    ```python
        self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
    >       self.assertEqual(
                calculator.add(0, 1),
                1
            )
    E       AssertionError: None != 1

    tests/test_calculator.py:11: AssertionError
    ================ short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - AssertionError: None != 1
    ================ 1 failed, 1 passed in 0.02s ==================
    ```
    This one is familiar. An `AssertionError` was the first error we solved in our test for failure.
    This is caused by the left side not being equal to the right side.
    Let's make them equal. update the `add` function in `calculator.py`
    ```python
    def add(x, y):
        return 1
    ```
    Eureka! The test passes
    ```python
    tests/test_calculator.py ..                                                                                                             [100%]

    ===================== 2 passed in 0.01s ======================
    ```
#### <span style="color:orange">**REFACTOR**</span>: Make it Better

Wait a minute. Is it that easy? Do we just provide the solution to make it pass? In the green phase, yes. We do whatever it takes to make the test pass even if we have to cheat.
This shows us that our test needs to be better.
What happens if our calculator users try to add other numbers?
What happens if our calculator users try to add a negative number?
Can we make it better?

- <span style="color:red">**RED**</span>: Write a failing test - update `test_calculator.py` with a new test
    ```python
    import unittest
    import calculator


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(0, 1),
                1
            )
            self.assertEqual(
                calculator.add(-1, 1),
                0
            )

    # TODO
    # test addition
    # test subtraction
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response

    ```python
    ======================= FAILURES =====================================
    _____________ TestCalculator.test_addition ___________________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
                calculator.add(0, 1),
                1
            )
    >       self.assertEqual(
                calculator.add(-1, 1),
                0
            )
    E       AssertionError: 1 != 0

    tests/test_calculator.py:15: AssertionError
    ================== short test summary info ===========================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - AssertionError: 1 != 0
    ================= 1 failed, 1 passed in 0.02s ========================
    ```
    Another AssertionError
- <span style="color:green">**GREEN**</span>: Make it Pass - update the `add` function in `calculator.py`
    ```python
    def add(x, y):
    return x + y
    ```
    terminal response
    ```
    tests/test_calculator.py ..                      [100%]

    ====================== 2 passed in 0.01s ==============
    ```
- <span style="color:orange">**REFACTOR**</span>: Make it Better

    let's randomize the inputs to make sure the function behaves the way we expect for any integers.
    update `test_calculator.py` to use the [random](https://docs.python.org/3/library/random.html?highlight=random#module-random) library
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
                calculator.add(x, y),
                x+y
            )

    # TODO
    # test addition
    # test subtraction
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    - set a variable x to a random integer between -1 and 1
    - set a variable y to a random integer between -1 and 1
    - test that when you give these two variables to the `add` function you get a sum of the 2 variables back

    terminal response
    ```
    tests/test_calculator.py ..           [100%]

    ================ 2 passed in 0.01s ===========================
    ```
    - we no longer need the previous 2 tests because this new test covers those cases and more
    - remove `test addition` from the TODO list since it passed and the task is completed

That's the pattern <span style="color:red">**RED**</span> <span style="color:green">**GREEN**</span> <span style="color:orange">**REFACTOR**</span>

---


### Test Subtraction

Let's add the other tests
#### <span style="color:red">**RED**</span> - write a failing test

- update `test_calculator.py` with `test_subtraction`
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
                calculator.add(x, y),
                x+y
            )

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
                calculator.subtract(x, y),
                x-y
            )

    # TODO
    # test subtraction
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response - AttributeError
    ```python

    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
    >           calculator.subtract(x, y),
                x-y
            )
    E       AttributeError: module 'calculator' has no attribute 'subtract'

    tests/test_calculator.py:23: AttributeError
    =============== short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - AttributeError: module 'calculator' has no attribute 'subtract'
    ============== 1 failed, 2 passed in 0.03s ==================
    ```
    update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    subtract = None
    ```
    terminal response - TypeError
    ```python
    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
    >           calculator.subtract(x, y),
                x-y
            )
    E       TypeError: 'NoneType' object is not callable

    tests/test_calculator.py:23: TypeError
    =================== short test summary info =============
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - TypeError: 'NoneType' object is not callable
    =============== 1 failed, 2 passed in 0.02s ============
    ```
    update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    def subtract():
        return None
    ```
    terminal response - TypeError
    ```python
    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
    >           calculator.subtract(x, y),
                x-y
            )
    E       TypeError: subtract() takes 0 positional arguments but 2 were given

    tests/test_calculator.py:23: TypeError
    =================== short test summary info ============================
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - TypeError: subtract() takes 0 positional arguments but 2 were given
    =================== 1 failed, 2 passed in 0.02s =========================
    ```

#### <span style="color:green">**GREEN**</span> - make it pass

- update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    def subtract(x, y):
        return None
    ```
    terminal response - AssertionError
    ```python
    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
    >       self.assertEqual(
                calculator.subtract(x, y),
                x-y
            )
    E       AssertionError: None != 0

    tests/test_calculator.py:22: AssertionError
    ================= short test summary info ===================
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - AssertionError: None != 0
    ================ 1 failed, 2 passed in 0.02s ================
    ```
    update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y
    ```
    terminal response - SUCCESS!
    ```shell
    collected 3 items

    tests/test_calculator.py ...                          [100%]

    ======================= 3 passed in 0.01s ==================
    ```
- remove `test subtraction` from the TODO list

#### <span style="color:orange">**REFACTOR**</span> - make it better

- How can we make this better?
- Is there any duplication that could be removed? Yes
    - `x = random.randint(-1, 1)` happens 2 times
    - `y = random.randint(-1, 1)` happens 2 times


- update `test_calculator.py`
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

    # TODO
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response stays the same
    the x and y variables are now initialized as class variables that can be referenced later using `self.x` and `self.y`

---

### Test Multiplication

#### <span style="color:red">**RED**</span> - write a failing test

update `test_calculator.py` with `test_multiplication`
```python
import unittest
import calculator
import random


class TestCalculator(unittest.TestCase):

    x = random.randint(-1, 1)
    y = random.randint(-1, 1)

    def test_failure(self):
        self.assertTrue(True)

    def test_addition(self):
        self.assertEqual(
            calculator.add(self.x, self.y),
            self.x+self.y
        )

    def test_subtraction(self):
        self.assertEqual(
            calculator.subtract(self.x, self.y),
            self.x-self.y
        )

    def test_multiplication(self):
        self.assertEqual(
            calculator.multiply(self.x, self.y),
            self.x*self.y
        )

# TODO
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
# AttributeError
# TypeError
```
terminal response - AttributeError

#### <span style="color:green">**GREEN**</span> - make it pass
update `calculator.py`
```python
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y
```
terminal response - SUCCESS
#### <span style="color:orange">**REFACTOR**</span> - make it better

- remove `test_multiplication` from the TODO list
- Can you think of any way to make the code better?

---

### Test Division

#### <span style="color:red">**RED**</span> - write a failing test
- update `test_calculator.py` with `test_division`
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            self.assertEqual(
                calculator.divide(self.x, self.y),
                self.x/self.y
            )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response - AttributeError
- update `calculator.py` with `divide`
    ```python
    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y

    def multiply(x, y):
        return x * y

    def divide(x, y):
        return x / y
    ```
    terminal response may vary. When y is 0 we get a [ZeroDivisionError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#ZeroDivisionError)
    ```python
    x = 1, y = 0

        def divide(x, y):
    >       return x / y
    E       ZeroDivisionError: division by zero

    calculator.py:11: ZeroDivisionError
    ================= short test summary info ========================
    FAILED tests/test_calculator.py::TestCalculator::test_division - ZeroDivisionError: division by zero
    ==================== 1 failed, 4 passed in 0.03s =================
    ```
    add `ZeroDivisionError` to the list of errors encountered

##### How to test for Errors
- <span style="color:red">**RED**</span> - write a failing test
    - update `test_calculator.py` with a test for division by zero
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            self.assertEqual(
                calculator.divide(self.x, 0),
                self.x/0
            )
            # self.assertEqual(
            #     calculator.divide(self.x, self.y),
            #     self.x/self.y
            # )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    # ZeroDivisionError
    ```
    terminal response
    ```python
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    x = 0, y = 0

        def divide(x, y):
    >       return x / y
    E       ZeroDivisionError: division by zero

    calculator.py:11: ZeroDivisionError
    ================= short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_division - ZeroDivisionError: division by zero
    =================== 1 failed, 4 passed in 0.02s ================
    ```

- <span style="color:green">**GREEN**</span> - make it pass
    - update `test_calculator.py` to confirm that `ZeroDivisionError` is raised when dividing by 0
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            with self.assertRaises(ZeroDivisionError):
                calculator.divide(self.x, 0)
            # self.assertEqual(
            #     calculator.divide(self.x, self.y),
            #     self.x/self.y
            # )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    # ZeroDivisionError
    ```
    terminal response - SUCCESS - We now have a way to `catch` Exceptions in testing, allowing tests to continue when they encounter expected failures

- <span style="color:orange">**REFACTOR**</span> - make it better
    - update `test_calculator.py` to test other division cases when the divisor is not 0 by adding a while condition
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            with self.assertRaises(ZeroDivisionError):
                calculator.divide(self.x, 0)
            while self.y == 0:
                self.y = random.randint(-1, 1)
            self.assertEqual(
                calculator.divide(self.x, self.y),
                self.x/self.y
            )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    # ZeroDivisionError
    ```
    - `while self.y == 0:` this creates a loop, you are telling python to repeat the block that follows as long as `self.y is equal to 0`
    - remove `test_division` from `TODO`

---

***CONGRATULATIONS*** You made it through writing a program that can perform the 4 basic arithmetic operations using Test Driven Development
