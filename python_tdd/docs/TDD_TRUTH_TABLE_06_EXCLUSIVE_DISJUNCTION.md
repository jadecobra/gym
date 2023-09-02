# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

### Exclusive Disjunction

#### <span style="color:red">**RED**</span>: make it fail

add a test for exclusive disjunction to `TestBinaryOperations`

```python
    def test_exclusive_disjunction(self):
        self.assertFalse(truth_table.exclusive_disjunction(True, True))
        self.assertTrue(truth_table.exclusive_disjunction(True, False))
        self.assertTrue(truth_table.exclusive_disjunction(False, True))
        self.assertFalse(truth_table.exclusive_disjunction(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- add a definition with a condition for the first case
    ```python
    def exclusive_disjunction(p, q):
        if p == True and q == True:
            return True
    ```
    we get an [AssertionError](./04_ASSERTION_ERROR.md)
- change the return statement
    ```python
            return False
    ```
- on to the next case
    ```python
    def exclusive_disjunction(p, q):
        if p == True and q == True:
            return False
        if p == True and q == False:
            return True
    ```
- onward to the 3rd case
    ```python
    def exclusive_disjunction(p, q):
        if p == True and q == True:
            return False
        if p == True and q == False:
            return True
        if p == False and q == True:
            return True
    ```
    all tests pass. Fantastic!

#### <span style="color:orange">**REFACTOR**</span>: make it better

Let's try to refactor those statements to make them better

- in the first case `p` and `q` have the same value, can we change the statement to reflect this like we did with `logical_equality`?
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        if p == True and q == False:
            return True
        if p == False and q == True:
            return True
    ```
    tests still pass
- the other 2 statements both return `True` and `p` and `q` are opposite of each other in both cases, we can rewrite that as
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        if p != q:
            return True
        if p != q:
            return True
    ```
    removing the repetition
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        if p != q:
            return True
    ```s
- we reorder and replace a statement with an `else` since there are now only 2 case
    ```python
    def exclusive_disjunction(p, q):
        if p != q:
            return True
        else:
            return False
    ```
- rewriting it on one line
    ```python
    def exclusive_disjunction(p, q):
        return True if p != q else False
    ```
- using implicit conditional testing we rewrite it as
    ```python
    def exclusive_disjunction(p, q):
        return p != q
    ```

What do we know so far?
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