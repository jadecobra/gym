# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

# Truth Table

We know there are two boolean values - `True` and `False`. The truth table shows us the logical outcomes of interactions between the two. It will give us practice in writing conditional statements

## Binary Operations - It takes 2 to tango

Let's test the 16 outcomes of binary operations

### Logical Conjunction

#### <span style="color:red">**RED**</span>: make it fail

create a `TestCase` for binary operations in `test_truth_table.py`

```python


class TestBinaryOperations(unittest.TestCase):

    def test_logical_conjunction(self):
        self.assertTrue(truth_table.logical_conjunction(True, True))
        self.assertFalse(truth_table.logical_conjunction(True, False))
        self.assertFalse(truth_table.logical_conjunction(False, True))
        self.assertFalse(truth_table.logical_conjunction(False, False))
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- add a definition for `logical_conjunction` to `truth_table.py`
    ```python
    def logical_conjunction():
        return None
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md)
- update the function signature with a positional argument
    ```python
    def logical_conjunction(p):
        return None
    ```
    the terminal updates to show another [TypeError](./03_TYPE_ERROR.md)
- add another positional argument
    ```python
    def logical_conjunction(p, q):
        return None
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update `logical_conjunction` in `truth_table.py`
    ```python
    def logical_conjunction(p, q):
        return True
    ```
    this makes the first of the four tests pass. the terminal updates to show the second line fails
- how can we make this function return different values based on the input it receives? we can use [if statements](https://docs.python.org/3/tutorial/controlflow.html?highlight=statement#if-statements)
- add an `if statement` for the first case `self.assertTrue(truth_table.logical_conjunction(True, True))` where p is `True` and q is `True`
    ```python
    def logical_conjunction(p, q):
        if p == True:
            return True
    ```
    the terminal still shows an [AssertionError](./04_ASSERTION_ERROR.md)
- let's add a condition for the second input value
    ```python
    def logical_conjunction(p, q):
        if p == True:
            if q == True:
                return True
    ```
    the test updates to show passing tests. Lovely!


#### <span style="color:orange">**REFACTOR**</span>: make it better

- Why does this work? We didn't define an alternate condition, just the one that returns `True` when p is `True` and q is `True`
- Is the function somehow implicitly returning `False`? In other words `is None False?`. We know the answer to this from [data structures](./06_DATA_STRUCTURES.md), let's test it as a reminder. add an explicit statement to the definition of `logical_conjunction`
    ```python
    def logical_conjunction(p, q):
        if p == True:
            if q == True:
                return True
        if p != True:
            if q != True:
                return False
    ```
    we have now explicitly stated the condition for all 4 cases. In one case when both `p ` and `q` are `True`, the function returns `True` and in every other case it returns `False`. Is there a better way to say this? We can use `else`. Update the `logical_conjunction` function
    ```python
    def logical_conjunction(p, q):
        if p == True:
            if q == True:
                return True
        else:
            return False
    ```
    we have reduced the amount of code and still get the same result. Is it better than what we had before? what else can we change?
- in python the [if statement]((https://docs.python.org/3/tutorial/controlflow.html?highlight=statement#if-statements) implicitly checks if something is `True`, which means we can refactor `if x == True` to `if x`. Both statements are the same. Knowing this we update `logical_conjunction`
    ```python
    def logical_conjunction(p, q):
        if p:
            if q:
                return True
        else:
            return False
    ```
    the terminal updates to show passing tests
- there's one last thing we can do, we can use the `and` operator to represent our nested conditions. Let's try it.
    ```python
    def logical_conjunction(p, q):
        if p and q:
            return True
        else:
            return False
    ```
- there's one more way we can represent this conditional. python allows for returning a conditional so we can say the above in one line
    ```python
    def logical_conjunction(p, q):
        return True if p and q else False
    ```
    the terminal shows passing tests
- python also can return the evaluation of the condition, try this
    ```python
    def logical_conjunction(p, q):
        return p and q
    ```
    the terminal shows passing tests

***FANTASTIC!*** You have tested logical_conjunction which is a conditional operation using `and`. We now know that
- `logical_conjunction` is `and`
- `False` is `not True`
- `True` is `not False`
- `False` is `False`
- `True` is `True`