# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

### Logical NAND

#### <span style="color:red">**RED**</span>: make it fail

add a test for exclusive disjunction to `TestBinaryOperations`

```python
    def test_logical_nand(self):
        self.assertFalse(truth_table.logical_nand(True, True))
        self.assertTrue(truth_table.logical_nand(True, False))
        self.assertTrue(truth_table.logical_nand(False, True))
        self.assertTrue(truth_table.logical_nand(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)


#### <span style="color:green">**GREEN**</span>: make it pass

- add a definition for the function to `truth_table.py` with a condition for the first case
    ```python
    def logical_nand(p, q):
        if p == True and q == True:
            return True
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the first case
- update the condition to return `False`
    ```python
            return False
    ```
    the terminal shows an [AssertionError](./04_ASSERTION_ERROR.md) for the second case
- add a condition for the second case
    ```python
    def logical_nand(self):
        if p == True and q == True:
            return False
        if p == True and q == False:
            return True
    ```
- add a condition for the 3rd case
    ```python
    def logical_nand(self):
        if p == True and q == True:
            return False
        if p == True and q == False:
            return True
        if p == False and q == True:
            return True
    ```
- one more for the 4th case
    ```python
    def logical_nand(self):
        if p == True and q == True:
            return False
        if p == True and q == False:
            return True
        if p == False and q == True:
            return True
        if p == False and q == False:
            return True
    ```
    We are green! All tests pass

#### <span style="color:orange">**REFACTOR**</span>: make it better

- Looking at the four conditions we have, 3 of them return exactly the same thing and we know there are only 2 outcomes, either `True` or `False`. Let's state the 3 statements as an else
    ```python
    def logical_nand(p, q):
        if p == True and q == True:
            return False
        else:
            return True
    ```
- we can use implicit conditional checking to rewrite the `if` statement
    ```python
    def logical_nand(p, q):
        if p and q:
            return False
        else:
            return True
    ```
- restate the `else` clause as the opposite of the `if` statement
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
- restate the second statement with `else`
    ```python
    def logical_nand(p, q):
        if not(p and q):
            return True
        else:
            return False
    ```
- rewrite it to one line
    ```python
    def logical_nand(p, q):
        return True if not(p and q) else False
    ```
- simplify using implicit conditional
    ```python
    def logical_nand(p, q):
        return not(p and q)
    ```

Let's update our knowledge

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