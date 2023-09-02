# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

### Logical Disjunction

#### <span style="color:red">**RED**</span>: make it fail

add a test for logical disjunction to `TestBinaryOperations` in `test_truth_table.py`

```python
    def test_logical_disjunction(self):
        self.assertTrue(truth_table.logical_disjunction(True, True))
        self.assertTrue(truth_table.logical_disjunction(True, False))
        self.assertTrue(truth_table.logical_disjunction(False, True))
        self.assertFalse(truth_table.logical_disjunction(False, False))
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- update `truth_table.py` with a function definition like we did for `logical_conjunction`
    ```python
    def logical_disjunction(p, q):
        return True
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- 3 of the test cases are passing because `logical_disjunction` returns `True` in 3 of the 4. We need a condition for the fourth case to pass. update the definition
    ```python
    def logical_disjunction(p, q):
        if p == False:
            if q == False:
                return False
        return True
    ```
    the terminal updates to show passing tests

#### <span style="color:orange">**REFACTOR**</span>: make it better

- we know from earlier that when we have a nested if statement it can be replaced with an `and`, so we update our condition
    ```python
    def logical_disjunction(p, q):
        if p == False and q == False:
            return False
        return True
    ```
    the terminal shows our tests are still passing
- we also know from earlier that we can return the entire condition in one line
    ```python
    def logical_disjunction(p, q):
        return False if p == False and q == False else return True
    ```
    the terminal still shows passing tests
- let's rewrite the statement to use `True` instead of `False` since we know from earlier that python implicitly checks if a conditional statement is `True`
    ```python
    def logical_disjunction(p, q):
        return False if p != True and q != True else True
    ```
    the terminal shows tests are still passing
- in `test_logical_negation` we learned we can use `not` to represent the opposite of a `boolean` so we can use it here
    ```python
    def logical_disjunction(p, q):
        return False if not p and not q else True
    ```
    the terminal shows passing tests
- there is some duplication in the statement, can we abstract the `not`?
    ```python
    def logical_disjunction(p, q):
        return False if (not p and not q) else True
    ```
    the terminal shows passing tests
- we abstract `not` from inside the parentheses to "multiply" the internals
    ```python
    def logical_disjunction(p, q):
        return False if not (p and q) else True
    ```
    the terminal shows a failing test. OOPS! If we expand our statement using "multiplication" rules. What we have above is
    ```python
        return False if not p not and not q else True
    ```
    this is not what we had in the beginning, we forgot to "multiply" `not` with the opposite of `and`. What is the opposite of and? `or`.
- let's update the statement with an `or` to see if it works
    ```python
    def logical_disjunction(p, q):
        return False if not (p or q) else True
    ```
    the terminal shows passing tests
- okay, can we do better? we have `False`, `not` and `True`, can we restate the statement in a way that uses less words? what if we restate the condition in terms of `True`. Let's unpack the statement to see if we can do better
    ```python
    def logical_disjunction(p, q):
        if not (p or q):
            return False
        else:
            return True
    ```
    tests are still passing. We could also say this as
    ```python
    def logical_disjunction(p, q):
        if not (p or q):
            return False
        if p or q:
            return True
    ```
    we are still green
- what happens if state the `True` case first?
    ```python
    def logical_disjunction(p, q):
        if p or q:
            return True
        if not(p or q):
            return False
    ```
    the tests pass
- what if we change the `False` condition to an `else`
    ```python
    def logical_disjunction(p, q):
        if p or q:
            return True
        else:
            return False
    ```
    we can now restate it on one line
    ```python
    def logical_disjunction(p, q):
        return True if p or q else False
    ```
    which also means we can restate it since we know python evaluates if statements against `True`
    ```python
    def logical_disjunction(p, q):
        return p or q
    ```
    Could this have been done in less steps?

***VOILA!*** the tests still pass and we have a simple statement that makes all 4 states pass for `logical_disjunction` or `or`
Our knowledge is updated to
- `and` is "not `or`"
- `or` is "not `and`"
- `logical_disjunction` is `or`
- `logical_conjunction` is `and`
- `False` is `not True`
- `True` is `not False`
- `False` is `False`
- `True` is `True`