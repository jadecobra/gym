# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

# Truth Table

We know there are two boolean values - `True` and `False`. The truth table shows us the logical outcomes of interactions between the two. It will give us practice in writing conditional statements

### Logical Equality/Logical Bi-conditional

#### <span style="color:red">**RED**</span>: make it fail

add a test for logical equality to `TestBinaryOperations`

```python
    def test_logical_equality_aka_logical_biconditional(self):
        self.assertTrue(truth_table.logical_equality(True, True))
        self.assertFalse(truth_table.logical_equality(True, False))
        self.assertFalse(truth_table.logical_equality(False, True))
        self.assertTrue(truth_table.logical_equality(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- add a definition to `truth_table.py` with a condition for the first case
    ```python
    def logical_equality(p, q):
        if p == True and q == True:
            return True
    ```
    the terminal updates to show 3 cases pass and the 4th case fails
- add a condition for it
    ```python
    def logical_equality(p, q):
        if p == True and q == True:
            return True
        if p == False and q == False:
            return True
    ```
    lovely! the tests pass

#### <span style="color:orange">**REFACTOR**</span>: make it better

What can we do to make this better?

- Let's simplify the 2 statements. In statement 1 `p` and `q` have the same value so we could change our condition to reflect that
    ```python
    def logical_equality(p, q):
        if p == q:
            return True
        if p == False and q == False:
            return True
    ```
    wait a minute, the second statement looks exactly the same
    ```python
    def logical_equality(p, q):
        if p == q:
            return True
        if p == q:
            return True
    ```
    remove the repetition
    ```python
    def logical_equality(p, q):
        if p == q:
            return True
    ```
    all tests still pass
- let's write it as a one line return statement
    ```python
    def logical_equality(p, q):
        return p == q
    ```
    all tests pass

We now know that
- `logical_equality` is `==`
- `logical_disjunction` is `or`
- `logical_conjunction` is `and`
- `and` is not `or`
- `or` is not `and`
- `False` is `not True`
- `True` is `not False`
- `False` is `False`
- `True` is `True`