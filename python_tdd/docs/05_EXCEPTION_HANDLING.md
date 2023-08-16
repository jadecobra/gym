# How to handle Exceptions in python

This tutorial will step through handling Exceptions in python using Test Driven Development

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

In [TDD_CALCULATOR](./TDD_CALCULATOR.md), we built a calculator and ran into issues when dividing by zero. In Mathematics, dividing by zero is undefined and in python it raises a `ZeroDivisionError`. To solve that problem we modified the test to do something else if the divisor was ever 0. Let's take a different approach.
- What if we want the program to return a message instead of ending execution of the program abruptly?
- What if we want to asset that dividing by zero causes an error but the error it causes does not end our tests?

### How to test that an Exception is raised

#### <span style="color:red">**RED**</span>: Write a failing test

create a file named `test_exception_handling.py` in the `tests` folder and add the following

```python
import unittest


class TestExceptionHandling(unittest.TestCase):

    def test_catching_module_not_found_error_in_tests(self):
        import non_existent_module
```
the terminal updates to show `ModuleNotFoundError`. We know one solution is to create the module, but in this case we want to catch/handle the exception in the test as a way to prove in the code that a `ModuleNotFoundError` will be raised for this module `non_existent_module` that does not exist

#### <span style="color:green">**GREEN**</span>: Make it Pass

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

Let's 


We create a file named `exceptions.py` in `project_name` to make it pass

### <span style="color:orange">**REFACTOR**</span> - make it better