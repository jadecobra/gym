# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

### Converse NonImplication

#### <span style="color:red">**RED**</span>: make it fail

add a test for converse nonimplication to `TestBinaryOperations`

```python
    def test_converse_nonimplication(self):
        self.assertFalse(truth_table.converse_nonimplication(True, True))
        self.assertFalse(truth_table.converse_nonimplication(True, False))
        self.assertTrue(truth_table.converse_nonimplication(False, True))
        self.assertFalse(truth_table.converse_nonimplication(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def converse_nonimplication(p, q):
        return False
    ```
    since the first two cases pass, the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- add a condition for the third case
    ```python
    def converse_nonimplication(p, q):
        if p == False and q == True:
            return True
        return False
    ```
    all the tests pass

#### <span style="color:orange">**REFACTOR**</span>: make it better
