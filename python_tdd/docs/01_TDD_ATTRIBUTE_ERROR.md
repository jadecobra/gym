# How to solve the AttributeError in Python

This tutorial will step through solving an `AttributeError`` in Python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Attributes

Attributes are properties/variables/names that belong to an object
You get an `AttributeError` when you reference an attribute that does not exist

### <span style="color:red">**RED**</span>: Write a failing test

Open a new file in your editor and save it as `test_attribute_error.py` in the `tests` folder you created in [Setup Test Driven Development Project](./TDD_SETUP.md)
Type the following in the file

```python
import unittest
import module


class TestAttributeError(unittest.TestCase):
    def test_defining_variables_to_solve_attribute_errors(self):
        self.assertIsNone(module.attribute_0)
```

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

We've seen this error before in [00_TDD_MODULE_NOT_FOUND_ERROR](./00_TDD_MODULE_NOT_FOUND_ERROR.md) and know how to solve it.

### <span style="color:green">**GREEN**</span>: Make it Pass

- create `module.py` in the `project_name` folder
- your terminal will update to show the following

```shell
self = <tests.test_attribute_error.TestAttributeError testMethod=test_defining_variables_to_solve_attribute_errors>

    def test_defining_variables_to_solve_attribute_errors(self):
>       self.assertIsNone(module.attribute_0)
E       AttributeError: module 'module' has no attribute 'attribute_0'

tests/test_attribute_error.py:7: AttributeError
```

Looking at the traceback starting from the bottom
- `tests/test_attribute_error.py:7: AttributeError` the location of the failure