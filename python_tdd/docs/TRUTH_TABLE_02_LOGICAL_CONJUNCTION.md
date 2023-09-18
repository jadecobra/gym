# How to write conditions in python

We will continue to step through learning conditional statements in python using Test Driven Development using the [Truth Table](https://en.wikipedia.org/wiki/Truth_table)

We know that there are two boolean values
- `True`
- `False`

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

# Binary Operations - It takes 2 to tango

Let's test the 16 outcomes of binary operations

## Logical Conjunction

### <span style="color:red">**RED**</span>: make it fail

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

### <span style="color:green">**GREEN**</span>: make it pass

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
- add an [if statement](https://docs.python.org/3/reference/compound_stmts.html?highlight=return%20true#the-if-statement) for the first case `self.assertTrue(truth_table.logical_conjunction(True, True))` where p is `True` and q is `True`
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


### <span style="color:orange">**REFACTOR**</span>: make it better

- Why does this work?
    - we add a condition for when the value of `p` is equal to `True` and inside that condition we have another for when the value of `q` is equal to `True`
    - if both conditions are met, the `logical_conjunction` function returns True but what does it do when those two conditions are not met?
- we know by default a function returns `None` so it must be returning `None` for the other cases. Does this mean `None` is `False`? We know the answer to this from [data structures](./06_DATA_STRUCTURES.md), let's test it as a reminder. add another return statement to the definition of `logical_conjunction`
    ```python
    def logical_conjunction(p, q):
        if p == True:
            if q == True:
                return True
        return None
    ```
    tests are still passing
- if `None` is `False` we can be more explicit by using the boolean `False`
    ```python
    def logical_conjunction(p, q):
        if p == True:
            if q == True:
                return True
        return False
    ```
    tests still pass
- can we express these nested conditionals as one line? yes, we can use the `and` keyword
    ```python
    def logical_conjunction(p, q):
        if p == True and q == True:
            return True
        return False
    ```
    still green
- we can rewrite the opposite of the `if` statement by using the `else` keyword
    ```python
    def logical_conjunction(p, q):
        if p == True and q == True:
            return True
        else:
            return False
    ```
    tests are still green because this expresses all four cases from `test_logical_conjunction`
    - in 1 case where `p is True` and `q is True` it returns True
    - in the 3 remaining cases it returns False
    - this means in a binary operation with 2 outcomes we only need to write a condition for one and write an else for the other. This will save us having to write out a condition for every case
- python equality [comparisons](https://docs.python.org/3/reference/expressions.html?highlight=ternary%20conditional#comparisons) for booleans can be implicitly stated because python calls `bool()` on the values, e.g `if p == True` can be rewritten as `if p` so we can rewrite our `if` statement in a simpler way
    ```python
    def logical_conjunction(p, q):
        if p and q:
            return True
        else:
            return False
    ```
    our tests still pass, so far so good
- we can also express conditions in a return statement using [conditional expressions/ternary operators](https://docs.python.org/3/reference/expressions.html?highlight=ternary%20conditional#conditional-expressions)
    ```python
    def logical_conjunction(p, q):
        return True if p and q else False
    ```
- since python implicitly tests conditionals we can rewrite the statement this way
    ```python
    def logical_conjunction(p, q):
        return p and q
    ```
    things are still green. I don't think we can get a simpler statement than this

***FANTASTIC!*** You have tested logical_conjunction which is a conditional operation using `and`. We now know that for any boolean operation involving 2 inputs - `p` and `q` which can take the values `True` or `False`
- `return True if x else y` can be rewritten as `return x` if `x` evaluates to `True`
- when there are multiple outcomes we only need to write the condition for the special case and use `else` for the others
- `logical_conjunction` is `and`
- `False` is `not True`
- `True` is `not False`
- `False` is `False`
- `True` is `True`