# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Environment](./TDD_SETUP.md)

---

## Converse Implication

### <span style="color:red">**RED**</span>: make it fail

add a test for converse implication to `TestBinaryOperations`

```python
    def test_converse_implication(self):
        self.assertTrue(truth_table.converse_implication(True, True))
        self.assertTrue(truth_table.converse_implication(True, False))
        self.assertFalse(truth_table.converse_implication(False, True))
        self.assertTrue(truth_table.converse_implication(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def converse_implication(p, q):
        return False
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the first case
- change the return value
    ```python
    def converse_implication(p, q):
        return True
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the third case
- add a condition for it
    ```python
    def converse_implication(p, q):
        if p == False and q == True:
            return False
        else:
            return True
    ```
    all the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

- use implied conditional testing
    ```python
    def converse_implication(p, q):
        if not p and q:
            return False
        else:
            return True
    ```
    still passing
- change `else` to the opposite of the `if` statement
    ```python
    def converse_implication(p, q):
        if not p and q:
            return False
        if not(not p and q):
            return True
    ```
- "multiply" out the values in the second condition
    ```python
    def converse_implication(p, q):
        if not p and q:
            return False
        if not not p not and not q:
            return True
    ```
    the terminal shows a `SyntaxError`, fix the syntax
    ```python
    def converse_implication(p, q):
        if not p and q:
            return False
        if p or not q:
            return True
    ```
- reorder the statements
    ```python
    def converse_implication(p, q):
        if p or not q:
            return True
        if not p and q:
            return False
    ```
- replace the second condition with `else`
    ```python
    def converse_implication(p, q):
        if p or not q:
            return True
        else:
            return False
    ```
- simplify it to one line
    ```python
    def converse_implication(p, q):
        return p or not q
    ```
    You win again! All tests pass

Our knowledge has increased
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
