# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Logical Equality/Logical Bi-conditional

### <span style="color:red">**RED**</span>: make it fail

add a test for logical equality to `TestBinaryOperations`

```python
    def test_logical_equality_aka_logical_biconditional(self):
        self.assertTrue(truth_table.logical_equality(True, True))
        self.assertFalse(truth_table.logical_equality(True, False))
        self.assertFalse(truth_table.logical_equality(False, True))
        self.assertTrue(truth_table.logical_equality(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a definition to `truth_table.py` with a return statement, we can pick `True` or `False` since 2 out of the 4 cases are either `True` or `False`
    ```python
    def logical_equality(p, q):
        return True
    ```
    the terminal updates to show the second case failing
- add a condition for it
    ```python
    def logical_equality(p, q):
        if p == True and q == False:
            return False
        return True
    ```
    the terminal shows a failure for the 3rd case
- add a condition
    ```python
    def logical_equality(p, q):
        if p == True and q == False:
            return False
        if p == False and q == True:
            return False
        return True
    ```
    We are green!

### <span style="color:orange">**REFACTOR**</span>: make it better

What can we do to make this better?

- looking at the test cases, we can summarize them as 2 states
    - logical_equality returns True when `p` and `q` are the same
    - logical_equality returns False when `p` and `q` are not the same
- we rewrite the condition statements to reflect the second observation
    ```python
    def logical_equality(p, q):
        if p != q:
            return False
        return True
    ```
- updating the function with the first observation we have
    ```python
    def logical_equality(p, q):
        if p != q:
            return False
        if p == q:
            return True
    ```
- reorder
    ```python
    def logical_equality(p, q):
        if p == q:
            return True
        if p != q:
            return False
    ```
- replace with `else`
    ```python
    def logical_equality(p, q):
        if p == q:
            return True
        else:
            return False
    ```
- rewrite as one line with the `return` statement
    ```python
    def logical_equality(p, q):
        return True if p == q else False
    ```
- use implicit condition comparison
    ```python
    def logical_equality(p, q):
        return p == q
    ```
    Well done! the tests are still green

Let's review
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