# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Environment](./TDD_SETUP.md)

---

## Negate First

### <span style="color:red">**RED**</span>: make it fail

add a test for negate first to `TestBinaryOperations`

```python
    def test_negate_first(self):
        self.assertFalse(truth_table.negate_first(True, True))
        self.assertFalse(truth_table.negate_first(True, False))
        self.assertTrue(truth_table.negate_first(False, True))
        self.assertTrue(truth_table.negate_first(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def negate_first(p, q):
        return False
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the third case
- before we add a condition for it, this looks similar to `logical_equality` and `exclusive_disjunction` because 2 out of the 4 cases have the same return value. We observe that
    - if `p == True` the result is `False`
    - if `p == False` the result is `True`
- let's add conditions to represent our observation
    ```python
    def negate_first(p, q):
        if p == True:
            return False
        if p == False:
            return True
    ```
    all the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

- use implied conditional testing
    ```python
    def negate_first(p, q):
        if p:
            return False
        if not p:
            return True
    ```
- reorder and use `else`
    ```python
    def negate_first(p, q):
        if not p:
            return True
        else:
            return False
    ```
- simplify
    ```python
    def negate_first(p, q):
        return not p
    ```
    ah, just like the name and all tests pass

## Negate Second

### <span style="color:red">**RED**</span>: make it fail

add a test for negate second to `TestBinaryOperations`

```python
    def test_negate_second(self):
        self.assertFalse(truth_table.negate_second(True, True))
        self.assertTrue(truth_table.negate_second(True, False))
        self.assertFalse(truth_table.negate_second(False, True))
        self.assertTrue(truth_table.negate_second(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def negate_second(p, q):
        return False
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the third case
- before we add a condition for it, this looks similar to `logical_equality`, `exclusive_disjunction` and `negate_first` because 2 out of the 4 cases have the same return value. We observe that
    - if `q == True` the result is `False`
    - if `q == False` the result is `True`
- let's try using our conclusion from `negate_first`
    ```python
    def negate_second(p, q):
        return not p
    ```
    the terminal still shows an [AssertionError](./04_ASSERTION_ERROR.md). Let's try `q` instead
    ```python
    def negate_second(p, q):
        return not q
    ```
    All tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

I don't think we can make it better. Let's update what we know so far

For any boolean operation involving 2 inputs - `p` and `q` which can take the values `True` or `False`
- `negate_first` always return `not p`
- `negate_second` always returns `not q`
- `material_non_implication` is `p and not q`
- `converse_non_implication` is `not p and q` which is different from `not(p and q)`
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