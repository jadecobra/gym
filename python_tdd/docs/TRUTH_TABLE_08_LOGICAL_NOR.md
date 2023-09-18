# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Logical NOR

### <span style="color:red">**RED**</span>: make it fail

add a test for exclusive disjunction to `TestBinaryOperations`

```python
    def test_logical_nor(self):
        self.assertFalse(truth_table.logical_nor(True, True))
        self.assertFalse(truth_table.logical_nor(True, False))
        self.assertFalse(truth_table.logical_nor(False, True))
        self.assertTrue(truth_table.logical_nor(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def logical_nor(p, q):
        return False
    ```
- the first 3 pass and we see a failure for the 4th case, let's add a condition for it
    ```python
    def logical_nor(p, q):
        if p == False and q == False:
            return True
        return False
    ```

### <span style="color:orange">**REFACTOR**</span>: make it better

- we restate the `if` condition using implicit conditional testing
    ```python
    def logical_nor(p, q):
        if not p and not q:
            return True
        return False
    ```
- we abstract the repetition of `not` by rewriting the entire statement in terms of `not`
    ```python
    def logical_nor(p, q):
        if not p not or not q:
            return True
        return False
    ```
    the terminal shows a `SyntaxError` and we rewrite the syntax properly
    ```python
    def logical_nor(p, q):
        if not(p or q):
            return True
        return False
    ```
- rewrite the entire thing on one line
    ```python
    def logical_nor(p, q):
        return True if not(p or q) else False
    ```
- simplify using implied conditional testing
    ```python
    def logical_nor(p, q):
        return not(p or q)
    ```
    BOOM! all the tests pass. Are we getting better at this?

Knowledge update. For any boolean operation involving 2 inputs - `p` and `q` which can take the values `True` or `False`
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