# How to write classes in python

This tutorial will step through learning the [Truth Table](https://en.wikipedia.org/wiki/Truth_table) in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

# Truth Table

We know there are two boolean values - `True` and `False`. The truth table shows us the logical outcomes of interactions between the two. It will give us practice in writing conditional statements

## Nullary Operations

These operations take in no inputs and always return the same value. They are singleton [functions](./07_FUNCTIONS.md)

#### <span style="color:red">**RED**</span>: make it fail

create a file named `test_truth_table.py` in the `tests` folder and add the following

```python
import unittest
import truth_table


class TestNullaryOperations(unittest.TestCase):

    def test_logical_true(self):
        self.assertTrue(truth_table.logical_true())
```
the terminal updates to show a [ModuleNotFoundError](./00_MODULE_NOT_FOUND_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- create a module named `truth_table.py` and the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add a singleton function named `logical_true`
    ```python
    def logical_true():
        return True
    ```
    the terminal updates to show passing tests
- We are reminded that `True` is `True`

#### <span style="color:orange">**REFACTOR**</span>: make it better

Let's add a test for `logical_false`

- add a test to `TestNullaryOperations`
    ```python
    def test_logical_false(self):
        self.assertFalse(truth_table.logical_false())
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add a function definition to `truth_table.py`
    ```python
    def logical_false():
        return False
    ```
    the terminal updates to show passing tests
- We are again reminded that
    - `True` is `True`
    - `False` is `False`


## Unary Operations

These take in one input and return the input, they are passthrough [functions](./07_FUNCTIONS.md)


#### <span style="color:red">**RED**</span>: make it fail

We add a new `TestCase` to `test_truth_table.py`

```python


class TestUnaryOperations(unittest.TestCase):

    def test_logical_identity(self):
        self.assertTrue(truth_table.logical_identity(True))
        self.assertFalse(truth_table.logical_identity(False))
```

the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

add a function definition to `truth_table.py`
```python
def logical_identity(value):
    return value
```
the terminal updates to show passing tests

#### <span style="color:red">**RED**</span>: make it fail

add a test for `logical_negation`
```python
    def test_logical_negation(self):
        self.assertFalse(truth_table.logical_negation(True))
        self.assertTrue(truth_table.logical_negation(False))
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- update `truth_table.py` with a definition for `logical_negation`
    ```python
    def logical_negation(value):
        return value
    ```
- the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md). The `logical_negation` function returns the value it receives as input. How do we make the function return the opposite of what it receives? use the `not` keyword
- update `logical_negation` to return the opposite of the `bool` value it returns
    ```python
    def logical_negation(value):
        return not value
    ```
    the terminal updates to show passing tests
- Reviewing what we know so far
    - `True` is `True`
    - `False` is `False`
    - `True` is `not False`
    - `False` is `not True`

## Binary Operations

Let's test the 16 outcomes of binary operations

### Logical Conjunction

##### <span style="color:red">**RED**</span>: make it fail

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
- Is the function somehow implicitly returning `False`? In other words `is None False?`. We know the answer to this from [DATA_STRUCTURES](./06_DATA_STRUCTURES.md), let's test it as a reminder. add an explicit statement to the definition of `logical_conjunction`
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
- `True` is `True`
- `False` is `False`
- `True` is `not False`
- `False` is `not True`
- `logical_conjunction` is `and`

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
    this is not what we had in the beginning, we forgot to "multiply" `not` with the opposite of `and` to get `not`. What is the opposite of and? it's `or`. let's update the statement with an `or` to see if it works
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
- `True` is `True`
- `False` is `False`
- `True` is `not False`
- `False` is `not True`
- `logical_conjunction` is `and`
- `logical_disjunction` is `or`

## Logical Implication/Material Implication

#### <span style="color:red">**RED**</span>: make it fail

add a test for logical implication to `TestBinaryOperations`

```python
    def test_logical_implication_aka_material_implication(self):
        self.assertTrue(truth_table.logical_implication(True, True))
        self.assertFalse(truth_table.logical_implication(True, False))
        self.assertTrue(truth_table.logical_implication(False, True))
        self.assertTrue(truth_table.logical_implication(False, False))
```

the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

#### <span style="color:green">**GREEN**</span>: make it pass

- add the function definition
    ```python
    def logical_implication(p, q):
        return True
    ```
    the terminal updates to show the second case failing
- add a condition for this case
    ```python
    def logical_implication(p, q):
        if p == True:
            if q == False:
                return False
        return True
    ```
    the tests pass!

#### <span style="color:orange">**REFACTOR**</span>: make it better

- How can we make this better? let's make the nested condition one line
    ```python
    def logical_implication(p, q):
        if p == True and q == False:
            return False
        return True
    ```
    the tests still pass
- in the earlier examples we replaced the equality tests with implied condition statements, let's try it here
    ```python
    def logical_implication(p, q):
        if p and not q:
            return False
        return True
    ```
    this looks simpler and the tests still pass.
- can we write the whole thing as one line?
    ```python
    def logical_implication(p, q):
        return False if p and not q else True
    ```
    fantastic!
- how can we make this even simpler? let's take a step back and see. If it fails we can always come back to what worked. Comment out the working line and add a new line
    ```python
    def logical_implication(p, q):
        # return False if p and not q else True
        if p and not q:
            return False
        else:
            return True
    ```
    it works.
- can we express the `else` part of the condition as a negation of the `if` portion?
    ```python
    def logical_implication(p, q):
        # return False if p and not q else True
        if p and not q:
            return False
        if not(p and not q):
            return True
    ```
    the tests pass
- Let's reorder the conditional statements
    ```python

    ```
