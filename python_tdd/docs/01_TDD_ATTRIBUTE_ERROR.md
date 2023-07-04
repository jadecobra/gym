# How to solve the AttributeError in Python

This tutorial will step through solving an `AttributeError`` in Python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Attributes

Attributes are properties/variables/names that belong to an object.
An `AttributeError` is raised when there is a reference an attribute/property/name/variable that does not exist in the object called

### <span style="color:red">**RED**</span>: Write a failing test

- Open a new file in the editor and save it as `test_attribute_error.py` in the `tests` folder you created in [Setup Test Driven Development Project](./TDD_SETUP.md) and type the following in the file

    ```python
    import unittest
    import module


    class TestAttributeError(unittest.TestCase):
        def test_defining_variables_to_solve_attribute_errors(self):
            self.assertIsNone(module.attribute_0)
    ```
    What is the code above doing?
    - `import unittest` imports the unittest module from the python standard library
    - `import module` import module from somewhere - this is going to hold the solution we write
    - `class TestAttributeError(unittest.TestCase):` - a class definition that inherits from `unittest.TestCase` and will hold our tests
    - `def test_defining_variables_to_solve_attribute_errors(self):` the definition of our first test function. we try to test one thing with our test function. In this case we are testing if definining variables can solve an `AttributeError`
    - `self.assertIsNone(module.attribute_0)` - the actual test. This is equivalent to asking the question `is module.attribute_0 equal to None`
    - `assertIsNone` is one of the helper functions inherited from `unittest.TestCase`
    - `self` refers to the `TestAttributeError` class

    If you left `pytest-watch` running from [Setup Test Driven Development Project](./TDD_SETUP.md) you should see the following in the terminal
    ```shell
    ImportError while importing test module '/<PATH_TO_PROJECT_NAME>/project_name/tests/test_attribute_error.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    /Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py:126: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
    tests/test_attribute_error.py:2: in <module>
        import module
    E   ModuleNotFoundError: No module named 'module'
    ```

    This error was encountered in [00_TDD_MODULE_NOT_FOUND_ERROR](./00_TDD_MODULE_NOT_FOUND_ERROR.md). We know how to solve it.

### <span style="color:green">**GREEN**</span>: Make it Pass

- create `module.py` in the `project_name` folder and the terminal will update to show the following
    ```shell
    self = <tests.test_attribute_error.TestAttributeError testMethod=test_defining_variables_to_solve_attribute_errors>

        def test_defining_variables_to_solve_attribute_errors(self):
    >       self.assertIsNone(module.attribute_0)
    E       AttributeError: module 'module' has no attribute 'attribute_0'

    tests/test_attribute_error.py:7: AttributeError
    ```
    Looking at the traceback starting from the bottom
    - `tests/test_attribute_error.py:7: AttributeError` the location and name of the Error that causes the failure
    - `E       AttributeError: module 'module' has no attribute 'attribute_0'` the module we imported has no definitions named `attribute_0`
    - `>       self.assertIsNone(module.attribute_0)` the line of code that errored out during execution
    - `def test_defining_variables_to_solve_attribute_errors(self):` the function definition where the error occurs
    - `self = <tests.test_attribute_error.TestAttributeError testMethod=test_defining_variables_to_solve_attribute_errors>` - A reference to the class and method(function) that caused the failure
- Open `module.py` in the Interactive Development Environment(IDE) and add the following
    ```python
    attribute_0
    ```
    The terminal will update to show the following
    ```shell
    tests/test_attribute_error.py:2: in <module>
        import module
    module.py:1: in <module>
        attribute_0
    E   NameError: name 'attribute_0' is not defined
    ```
    - `E   NameError: name 'attribute_0' is not defined` this is a new error so we add it to our running list of errors encountered. The running list now looks like this
        ```
        # Exceptions Encountered
        # AssertionError
        # ModuleNotFoundError
        # AttributeError
        # NameError
        ```
        A `NameError` is raised when there is a reference in an object with no definition
        - What is the difference between a `NameError` and an `AttributeError`?
            - An `AttributeError` occurs when there is a reference to a name in an object and the name does not exist e.g. `object.name`
            - A `NameError` occurs when there is a reference to name with no prior definition
        - What is similar between `ModuleNotFoundError`, `AttributeError` and `NameError`?
    - `attribute_0` the offending line
    - `module.py:1: in <module>` the location of the offending line
- Update `module.py` in the Interactive Development Environment(IDE) to
    ```python
    attribute_0 = None
    ```
    this explicity defines `attribute_0` with a value of `None` and the terminal updates to show a passing test
    ```shell
    collected 2 items

    tests/test_attribute_error.py .                                             [ 50%]
    tests/test_project_name.py .                                                [100%]

    ============================== 2 passed in 0.03s==================================
    ```

> ***What is the difference between `=` and `==` in python?***
> - `=` is used to assign names to objects e.g. `five = 5` means we can later refer to the number `5` with the name `five`
> - `==` is used to check if two things are equal e.g. `5 == 4` means we want to know if `5` is equal to `4`