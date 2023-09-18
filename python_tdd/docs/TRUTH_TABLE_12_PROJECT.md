# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Project First

### <span style="color:red">**RED**</span>: make it fail

add a test for project first to `TestBinaryOperations`

```python
    def test_project_first(self):
        self.assertTrue(truth_table.project_first(True, True))
        self.assertTrue(truth_table.project_first(True, False))
        self.assertFalse(truth_table.project_first(False, True))
        self.assertFalse(truth_table.project_first(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def project_first(p, q):
        return False
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) foe the first case
- change the return statement
    ```python
    def project_first(p, q):
        return True
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the third case
- before we add a condition for it, this looks similar to `logical_equality`, `exclusive_disjunction`, `negate_first` and `negate_second` because 2 out of the 4 cases have the same return value. We observe that
    - if `p == True` the result is `True`
    - if `p == False` the result is `False`
- let's add conditions to represent our observations
    ```python
    def project_first(p, q):
        if p == True:
            return True
        if p == False:
            return False
    ```
    all the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

- use implied conditional testing
    ```python
    def project_first(p, q):
        if p:
            return True
        if not p:
            return False
    ```
- simplify
    ```python
    def project_first(p, q):
        return True if p else False
    ```
- simplify further
    ```python
    def project_first(p, q):
        return p
    ```
    we are still green

## Project Second

### <span style="color:red">**RED**</span>: make it fail

add a test for project second to `TestBinaryOperations`

```python
    def test_project_second(self):
        self.assertTrue(truth_table.project_second(True, True))
        self.assertFalse(truth_table.project_second(True, False))
        self.assertTrue(truth_table.project_second(False, True))
        self.assertFalse(truth_table.project_second(False, False))
```

the terminal shows an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a function definition to `truth_table.py`
    ```python
    def project_second(p, q):
        return False
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the first case
- change the return value to make it pass
    ```python
    def project_second(p, q):
        return True
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the second case
- before we add a condition for it, this looks similar to `logical_equality`, `exclusive_disjunction`, `negate_first`, `negate_second` and `project_first` because 2 out of the 4 cases have the same return value. We observe that
    - if `q == True` the result is `True`
    - if `q == False` the result is `False`
- let's try using our conclusion from `project_first`
    ```python
    def project_second(p, q):
        return p
    ```
    the terminal still shows an [AssertionError](./04_ASSERTION_ERROR.md). Let's return `q` instead
    ```python
    def project_second(p, q):
        return q
    ```
    All tests pass and it's a simple line

### <span style="color:orange">**REFACTOR**</span>: make it better

Since there is no refactoring to do here, we update what we know so far. For any boolean operation involving 2 inputs - `p` and `q` which can take the values `True` or `False`
- `project_first` always returns `p`
- `project_second` always returns `q`
- `negate_first` always returns `not p`
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