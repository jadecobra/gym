# How to create a calculator using Test Driven Development

In this tutorial we will create a calculator using Test Driven Development. Let's begin

## Prerequisites

- [python](https://www.python.org/downloads/)
- an IDE - I use VSCode, there are other options
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

### Write a failing test

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

to test the code, write the following in the terminal

```shell
python -m unittest -f
```

you should get the following result