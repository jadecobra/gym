# How to Setup a Test Driven Development Environment

This tutorial will step through creating a Test Driven Development Environment in Python

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
    - [Other Interactive Development Environment(IDE) options](https://wiki.python.org/moin/IntegratedDevelopmentEnvironments)

## Setup

> ***Are you on a Windows machine?***
> - replace `touch` in the example below with `New-Item`
> - replace `python3` in the examples with `python`

### Setup File Structure

in a terminal type the following to setup the directory structure

```shell
mkdir -p project_name/tests
cd project_name
touch project_name.py
touch tests/__init__.py
touch tests/test_project_name.py
```

- `project_name` is a placeholder for the name of the project
- Tests are stored in the `tests` folder to separate them from the actual source code
- The `tests` folder contains `__init__.py` to tell python that this is a python package
- The actual test file is called `test_project_name.py`
- The module we are creating is called `project_name.py`
- What is a module? A python module is any file that ends in `.py`

---

### <span style="color:red">**RED**</span>: Write a failing test

- Open up `project_name/tests/test_project_name.py` in your Interactive Development Environment(IDE) and type the following
    ```python
    import unittest


    class TestProjectName(unittest.TestCase):

        def test_failure(self):
            self.assertFalse(True)
    ```
- `import unittest` imports an existing module from the python standard library that is used for testing.
- what is `unittest`? it is a module|library that comes with python for testing code
- what is the `TestProjectName` class? it is a "container" for the tests we are about to write
- what is `unittest.TestCase`? a class defined in the `unitest` library which contains a bunch of `methods|functions` for testing code that `TestProjectName` inherits so I do not have to rewrite them
- what is inheritance? a simple way to think of it is that `TestProjectName` is a child of `unittest.TestCase`
- what is `def test_failure`? it is the definition of a test function to test the system being built?
- what is `self`? self refers to the `TestProjectName` class. To access things within the `TestProjectName` class `self` is used. It avoids having to say `TestProjectName.assertFalse(True)`
- what is `self.assertFalse(True)`? an assert statement that is a substitute for `assert False == True` which is similar to asking the question `is False equal to True?`
- to test the code, write the following in the terminal
    ```shell
    python3 -m unittest
    ```
    you should get the following result
    ```python
    F
    ======================================================
    FAIL: test_failure (tests.TestProjectName.test_failure)
    ------------------------------------------------------
    Traceback (most recent call last):
    File "/<PATH_TO_PROJECT>/project_name/tests/test_project_name.py", line 7, in test_failure
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


    class TestProjectName(unittest.TestCase):

        def test_failure(self):
            self.assertFalse(True)

    # Exceptions Encountered
    # AssertionError
    ```
- `self.assertFalse(True)` the line of code that caused the failure
- `File "/<PATH_TO_CALCULATOR>/project_name/tests/test_project_name.py", line 7, in test_failure` where in the file the error occurred - line 7 in the `test_failure` function in the `test_project_name.py` file. Clicking on this line will place your cursor at the position in the Interactive Development Environment(IDE)
- `Traceback (most recent call last):` all the information returned by python is the traceback, showing the most recent call python made last.
- `FAIL: test_failure (tests.TestProjectName.test_failure)` a header giving information about the test
    - `tests.TestProjectName.test_failure` is the location of the failing test
      - `tests` - tests folder
      - `TestProjectName` - the class defined on line 4
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
- we will run `python3 -m unittest` again to make sure our improvements do not break previous passing tests

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
rootdir: <YOUR_PATH>/project_name
collected 1 item

tests/test_project_name.py .                                                                                                    [100%]

======================= 1 passed in 0.00s ============================
```

***CONGRATULATIONS*** You have successfully setup a Python Test Driven Environment and can build anything you want