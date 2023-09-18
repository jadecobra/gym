# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Logical NAND

### <span style="color:red">**RED**</span>: make it fail

add a test for exclusive disjunction to `TestBinaryOperations`

```python
    def test_logical_nand(self):
        self.assertFalse(truth_table.logical_nand(True, True))
        self.assertTrue(truth_table.logical_nand(True, False))
        self.assertTrue(truth_table.logical_nand(False, True))
        self.assertTrue(truth_table.logical_nand(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a definition for the function to `truth_table.py` returning `True` since 3 out of the 4 cases return that value
    ```python
    def logical_nand(p, q):
        return True
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the first case
- add a condition for the one case that returns `False`
    ```python
    def logical_nand(p, q):
        if p == True and q == True:
            return False
        return True
    ```
    We are green! All tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

- add an `else` to be explicit
    ```python
    def logical_nand(p, q):
        if p == True and q == True:
            return False
        else:
            return True
    ```
- change to an implied `if` statement
    ```python
    def logical_nand(p, q):
        if p and q:
            return False
        else:
            return True
    ```
- change it to the opposite of the `if` statement
    ```python
    def logical_nand(p, q):
        if p and q:
            return False
        if not(p and q):
            return True
    ```
- reorder
    ```python
    def logical_nand(p, q):
        if not(p and q):
            return True
        if p and q:
            return False
    ```
- replace second statement with `else`
    ```python
    def logical_nand(p, q):
        if not(p and q):
            return True
        else:
            return False
    ```
- return on one line
    ```python
    def logical_nand(p, q):
        return True if not(p and q) else False
    ```
- simplify to
    ```python
    def logical_nand(p, q):
        return not(p and q)
    ```
    I don't think we can get simpler than this and all the tests are still passing

***REVIEW***
We know that for any boolean operation involving 2 inputs - `p` and `q` which can take the values `True` or `False`
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
- `return True if x else y` can be rewritten as `return x` if `x` evaluates to `True`