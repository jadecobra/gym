# How to Setup a Test Driven Development Environment

This tutorial will step through creating a Test Driven Development Environment in python

Here's the Test Driven Development mantra paraphrased -
    <span style="color:red">**RED**</span> <span style="color:green">**GREEN**</span> <span style="color:orange">**REFACTOR**</span>
- <span style="color:red">**RED**</span>: make it fail
- <span style="color:green">**GREEN**</span>: make it pass
- <span style="color:orange">**REFACTOR**</span>: make it better

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
> - [install Git](https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.3/Git-2.41.0.3-32-bit.exe)
> - install WSLv2 by running the following in a terminal - `wsl --install`
> - run subsequent commands in WSL

### Setup File Structure

- type the following in a terminal to setup the directory structure
    ```shell
    mkdir -p project_name/tests
    cd project_name
    touch project_name.py
    touch tests/__init__.py
    touch tests/test_project_name.py
    ```
- `project_name` is a placeholder for the name of the project e.g. if you are building a project called `the_greatest_application`, replace `project_name` with `the_greatest_application`
- Tests are stored in the `tests` folder to separate them from the actual source code
- The `__init__.py` file in the `tests` folder tells python that this is a python package
- The actual test file is called `test_project_name.py`
- The module we are creating is called `project_name.py`
- What is a module? A python module is any file that ends in `.py`
- Your folder structure should look like this
    ```
    project_name
    |--tests
    |   |--__init__.py
    |   |--test_project_name.py
    |--project_name.py
    ```

---

## <span style="color:red">**RED**</span>: make it fail

- Open up `project_name/tests/test_project_name.py` in your Interactive Development Environment(IDE) and type the following
    ```python
    import unittest


    class TestProjectName(unittest.TestCase):

        def test_failure(self):
            self.assertFalse(True)
    ```
    - `import unittest` imports an existing module from the python standard library that is used for testing.
    - what is `unittest`? it is a module/library that comes with python for testing code
    - what is the `TestProjectName` class? it is a "container" for the tests we are about to write
    - what is `unittest.TestCase`? a class defined in the `unittest` library which contains a bunch of `methods/functions` for testing code that `TestProjectName` inherits so they do not have to be rewritten
    - what is inheritance? a simple way to think of it is that `TestProjectName` is a child of `unittest.TestCase`
    - what is `def test_failure`? it is the definition of a test function to test the system being built?
    - what is `self`? self refers to the `TestProjectName` class. To access things within the `TestProjectName` class `self` is used. It avoids having to say `TestProjectName.assertFalse(True)`
    - what is `self.assertFalse(True)`? an assert statement that is a substitute for `assert False == True` which is similar to asking the question `is False equal to True?`
- to test the code, write the following in the terminal
    ```shell
    python3 -m unittest
    ```
    the terminal updates to show
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

We follow the iterative process of <span style="color:red">**RED**</span> <span style="color:green">**GREEN**</span> <span style="color:orange">**REFACTOR**</span>

We are currently <span style="color:red">**RED**</span>.
The error provides important information about the code. Looking at it from the last line
- `FAILED (failures=1)` The test failed - <span style="color:red">**RED**</span>
- `Ran 1 test in 0.000s` python ran the 1 test written so far in 0.000s, the time might vary on your machine
- `AssertionError: True is not false` The error is an [AssertionError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#AssertionError). This is raised by python when an assert statement fails
- It further gives the False Assertion `True is not false`
- Keep a running tab of Errors aka Exceptions seen as you go through this exercise, they will help you be a better troubleshooter
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
- `Traceback (most recent call last):` all the information returned by python is the traceback, showing the most recent call python made last
- `FAIL: test_failure (tests.TestProjectName.test_failure)` a header giving information about the test
    - `tests.TestProjectName.test_failure` is the location of the failing test
      - `tests` - our tests folder
      - `TestProjectName` - the class defined on line 4
      - `test_failure` - the function defined on line 6
- `F` indicates a failure

---

## <span style="color:green">**GREEN**</span>: make it pass

- change line 7 to make the test pass. Which do you think is a better solution?
  - `self.assertTrue(True)` or
  - `self.assertFalse(False)`
- Why do you think it's a better solution?
- How did you make the decision?
- run the test again from the terminal
    ```shell
    python3 -m unittest
    ```
    the terminal updates to show
    ```shell
    .
    ------------------------------------------------------
    Ran 1 test in 0.000s

    OK
    ```

<span style="color:green">*CONGRATULATIONS!*</span> You have a passing test. We are <span style="color:green">**GREEN**</span>

---

## <span style="color:orange">**REFACTOR**</span>: make it better

We can make code better by using the
- [Abstraction Principle](https://en.wikipedia.org/wiki/Abstraction_principle_(computer_programming))
- [Do Not Repeat Yourself (DRY) Principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

So far there's not much to improve on what has been written but there has been duplication.
- we ran `python3 -m unittest` to see the test fail
- we ran `python3 -m unittest` to see the test pass
- we will run `python3 -m unittest` again to make sure our improvements do not break previous passing tests

This means for every test we introduce we have to run that command 3 times.
How do we avoid this repetition and focus on tests and solutions?

### How to Automatically Run Tests

#### How to Setup a Virtual Environment

> ***Are you on a Windows machine? If you are not using WSL***
> - replace `python3` in the examples with `python`
> - replace `source .venv/bin/activate` in the example below with `.venv/scripts/activate`

- in your editor create a file named `requirements.txt` and this line
    ```python
    pytest-watch
    ```
- save the file
- type the following in the terminal
    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install --requirement requirements.txt
    ```
    Your folder structure shoudl now look like this
    ```
    project_name
    |--.venv
    |--tests
    |   |--__init__.py
    |   |--test_project_name.py
    |--project_name.py
    |--requirements.txt
    ```

You just created a [virtual environment](https://docs.python.org/3/library/venv.html)
- `python3 -m venv .venv` creates a virtual environment named `.venv` - you can use any name you want
- what is [venv](https://docs.python.org/3/library/venv.html#module-venv)? a python module for creating virtual environments
- what is a virtual environment? an isolated `container/subfolder` that will hold any dependencies we install
- `source .venv/bin/activate` or `.venv/scripts/activate` activates the virtual environment
- `pip install --upgrade pip` - upgrades `pip` to the latest version
- what is pip? the [python package manager](https://pypi.org/project/pip/)
- `pip install --requirement requirements.txt` installs a python library named `pytest-watch` listed in the `requirements.txt`
- what is `pytest-watch`? a library that automatically runs tests when a change is made
- type `pytest-watch` in the terminal to run the tests. it updates to show
    ```shell
    [TODAYS_DATE] Running: py.test
    ======================= test session starts==========================
    platform <YOUR_OPERATING_SYSTEM> -- python <YOUR_python_VERSION >, pytest-<VERSION>, pluggy-<VERSION>
    rootdir: <YOUR_PATH>/project_name
    collected 1 item

    tests/test_project_name.py .                                                                                                    [100%]

    ======================= 1 passed in 0.00s ============================
    ```

> ***NOTE***
> #### How To activate a virtual environment when one exists
> - Open your terminal
> - change directory to <PROJECT_NAME>
> - activate the virtual environment by typing `source .venv/bin/activate`

***CONGRATULATIONS!*** You have successfully setup a python Test Driven Environment and can build anything you want. Go forth and conquer the world