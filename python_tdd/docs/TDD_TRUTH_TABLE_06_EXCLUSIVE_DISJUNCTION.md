# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Exclusive Disjunction

### <span style="color:red">**RED**</span>: make it fail

add a test for exclusive disjunction to `TestBinaryOperations`

```python
    def test_exclusive_disjunction(self):
        self.assertFalse(truth_table.exclusive_disjunction(True, True))
        self.assertTrue(truth_table.exclusive_disjunction(True, False))
        self.assertTrue(truth_table.exclusive_disjunction(False, True))
        self.assertFalse(truth_table.exclusive_disjunction(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a definition that returns `True`
    ```python
    def exclusive_disjunction(p, q):
        return True
    ```
    we get an [AssertionError](./04_ASSERTION_ERROR.md) for the second case
- add a condition for it
    ```python
    def exclusive_disjunction(p , q):
        if p == True and q == True:
            return False
        return True
    ```
    the terminal shows an [AssertionError](./04_ASSERTION_ERROR.md) for the fourth case
- add a condition
    ```python
    def exclusive_disjunction(p, q):
        if p == False and q == False:
            return False
        if p == True and q == True:
            return False
        return True
    ```
    Wonderful! All the tests are passing

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's try to refactor those statements to make them better

- in the first case `p` and `q` have the same value, can we change the statement to reflect this like we did with `logical_equality`?
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        if p == True and q == True:
            return False
        return True
    ```
    tests still pass
- the next statement looks similar, we can rewrite it as
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        if p == q:
            return False
        return True
    ```
    since it's exactly the same statement, we remove the repetition
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        return True
    ```
- add `else`
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        else:
            return True
    ```
- add the opposite `if` statement
    ```python
    def exclusive_disjunction(p, q):
        if p == q:
            return False
        if p != q:
            return True
    ```
- reorder
    ```python
    def exclusive_disjunction(p, q):
        if p != q:
            return True
        if p == q:
            return False
    ```
- replace with `else`
    ```python
    def exclusive_disjunction(p, q):
        if p != q:
            return True
        else:
            return False
    ```
- use one line return statement
    ```python
    def exclusive_disjunction(p, q):
        return True if p != q else False
    ```
- remove excess
    ```python
    def exclusive_disjunction(p, q):
        return p != q
    ```

What do we know so far?
- `exclusive_disjunction` is `!=`
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