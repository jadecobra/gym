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