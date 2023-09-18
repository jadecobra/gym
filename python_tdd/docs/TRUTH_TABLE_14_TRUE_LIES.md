# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Tautology

### <span style="color:red">**RED**</span>: make it fail

add a test for tautology to `TestBinaryOperations`

```python
    def test_tautology(self):
        self.assertTrue(truth_table.tautology(True, True))
        self.assertTrue(truth_table.tautology(True, False))
        self.assertTrue(truth_table.tautology(False, True))
        self.assertTrue(truth_table.tautology(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def tautology(p, q):
        return False
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the first case
- replace the return value
    ```python
    def tautology(p, q):
        return True
    ```
    all tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

Nothing to refactor here

## Contradiction

### <span style="color:red">**RED**</span>: make it fail

add a test for contradiction to `TestBinaryOperations`

```python
    def test_contradiction(self):
        self.assertFalse(truth_table.contradiction(True, True))
        self.assertFalse(truth_table.contradiction(True, False))
        self.assertFalse(truth_table.contradiction(False, True))
        self.assertFalse(truth_table.contradiction(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def contradiction(p, q):
        return True
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the first case
- update the return value
    ```python
    def contradiction(p, q):
        return False
    ```

### <span style="color:orange">**REFACTOR**</span>: make it better

Nothing to do here either. Let's update what we know so far

***YOU DID IT!***
For any boolean operation involving 2 inputs - `p` and `q` which can take the values `True` or `False`
- `contradition` always returns `False`
- `tautology` always returns `True`
- `converse_implication` is `not p and q` which is different from `not(p and q)`
- `logical_nor` is `not(p or q)`
- `logical_nand` is `not(p and q)`
- `exclusive_disjunction` is `!=` aka opposite of `logical_equality`
- `logical_equality` is `==`
- `logical_disjunction` is `or`
- `logical_conjunction` is `and`
- `and` is "not `or`"
- `or` is "not `and`"
- `False` is `not True`
- `True` is `not False`
- `False` is `False`
- `True` is `True`
