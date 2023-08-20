# Data Structures in python

This tutorial will cover data structures in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Data Structures

In programming we process input data of some form and output data in some form.
We can think of it as

```python
input_data -> program -> output_data
f(input_data) -> output_data # where f is the program|procress
```

## What are the data structures in python

- `None` - none - no value
- `bool` - boolean - True | False
- `int` - integers - positive/negative whole numbers e.g. -1, 0, 1
- `float` - floats - floating point numbers e.g. -1.1, 0.1, 1.1
- `str` - string - any text in strings"
- `tuple` - tuples - an immutable sequence of values
- `list` - lists - a mutable sequence of values
- `set` - sets - a sequence of values with no duplicates
- `dict` - dictionaries - a mapping of key, values

## What is None?

### <span style="color:red">**RED**</span>: Write a failing test

create a file named `test_data_structures.py` in the `tests` folder
```python
import unittest
```

### <span style="color:green">**GREEN**</span>: Make it Pass
### <span style="color:orange">**REFACTOR**</span> - make it better