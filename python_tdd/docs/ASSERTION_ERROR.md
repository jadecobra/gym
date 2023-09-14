# AssertionError

We will step through solving an [AssertionError](https://docs.python.org/3/library/exceptions.html?highlight=assertionerror#AssertionError) in python using Test Driven Development

### Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## What is an Assertion?

Is it some fundamental thing that we agree upon, a statement of fact or belief?

In python an `AssertionError` is raised when the result of an `assert` statement is `False`.
We are familiar with an `assert` statement from the first failing test we wrote in [Setup TDD](./TDD_SETUP.md)

```python
self.assertFalse(True)
```

which is another way of saying

```python
assert True is False
```

## Why are asserts important?

When building a program we have certain expectations based on given inputs.

One way to test these expectations is by adding `assert` statements to the program, we could also place them in tests to check whether our expectations match reality. These tests help us check that the system is doing what it was designed for and catch bugs that break previous behavior when introduced.

We are constantly asking
- What is similar?
- What is different?

The difference tells us what changes we can make for our expectations and reality to match.

## AssertionError with None

### <span style="color:red">**RED**</span>: make it fail

let us create a file in the `tests` folder named `test_assertion_error.py` add the following test using the python `assert` keyword

```python
import unittest


class TestAssertionError(unittest.TestCase):

    def test_assertion_errors_with_none(self):
        assert False is None
```

the terminal updates to show

```python
E       assert False is None

tests/test_assertion_error.py:7: AssertionError
```

This `AssertionError` is triggered by the line `assert None is False`, which is similar to the question "is `None` the same as `False`?". The difference here is that the `assert` at the beginning of the line makes the statement more like "DO NOT PROCEED UNLESS `None` is `False`". Since `None` and `False` are different objects and are not equal, python raises an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

we update `test_assertion_errors_with_none` in `test_assertion_error.py`

```python
        assert False is not None
```

and the terminal shows passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

Is there another way we can write `assert` statements?

- ##### <span style="color:red">**RED**</span>: make it fail
    let's add the following line to `test_assertion_errors_with_none` using the `unittest.TestCase.assertIsNone` method
    ```python
            self.assertIsNone(False)
    ```
    the terminal updates to show a more descriptive error
    ```python
    E       AssertionError: False is not None

    tests/test_assertion_error.py:8: AssertionError
    ```
    since `False is not None` we get an AssertionError

- #### <span style="color:green">**GREEN**</span>: make it pass
    let's update the assert statement to make it pass
    ```python
            self.assertIsNotNone(False)
    ```
    the terminal shows passing tests because this `assert` statement is `True`

    From our test we now know that in python
    - `False` is not `None`

    If `False` is not `None`, what is the relation of `None` to `True`? What test can we add to find out
- #### <span style="color:red">**RED**</span>: make it fail
    let's add another test to `test_assertion_errors_with_none`
    ```python
            assert True is None
    ```
    the terminal updates to show an `AssertionError`
    ```python
    E       assert True is None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_none` to make it pass
    ```python
            assert True is not None
    ```
    the terminal shows passing tests
- #### <span style="color:red">**RED**</span>: make it fail
    what if we rewrite the above statement using the `unittest.TestCase` equivalent method? update `test_assertion_errors_with_none`

    ```python
            self.assertIsNone(True)
    ```

    the terminal updates to show
    ```python
    E       AssertionError: True is not None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_none` to make it pass
    ```python
            self.assertIsNotNone(True)
    ```
    the terminal shows passing tests and we now know that in python
    - `False` is not `None`
    - `True` is not `None`

    Using what we know so far, what else can we discover and how can we use it to build programs?

- #### <span style="color:red">**RED**</span>: make it fail
    add another test to `test_assertion_errors_with_none`
    ```python
            assert None is not None
    ```
    the terminal updates to show
    ```python
    E       assert None is not None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_none` to make it pass
    ```python
            assert None is None
    ```
    the terminal updates to show passing tests
- #### <span style="color:red">**RED**</span>: make it fail
    let's add another test to `test_assertion_errors_with_none` using the `unittest.TestCase` method
    ```python
            self.assertIsNotNone(None)
    ```
    the terminal updates to show
    ```python
    >       self.assertIsNotNone(None)
    E       AssertionError: unexpectedly None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_none` to make it pass
    ```python
            self.assertIsNone(None)
    ```
    the terminal shows passing tests and we now know that in python
    - `False` is not `None`
    - `True` is not `None`
    - `None` is `None`

Which of the `assert` statements do you prefer when testing `None`?
- `assert x is None`
- `self.assertIsNone(x)`

Going with what we know so far, can we raise an `AssertionError` for things that are `False`?

## AssertionError with False

### <span style="color:red">**RED**</span>: make it fail

let's update `TestAssertionError` in `test_assertion_error.py` with the following test

```python
    def test_assertion_errors_with_false(self):
        assert True is False
```

the terminal updates to show
```python
E       assert True is False
```
### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_errors_with_false` to make it pass
```python
        assert False is False
```
the terminal updates to show passing tests

### <span style="color:red">**RED**</span>: make it fail
let's try the same test with the `unittest` equivalent method by updating `test_assertion_errors_with_false`

```python
        self.assertFalse(True)
```
the terminal updates to show
```python
E       AssertionError: True is not false
```
this test is familiar, it was the first failing test we wrote from [TDD Setup](./TDD_SETUP.md)

### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_error_with_false` to make it pass
```python
        self.assertFalse(False)
```
the terminal updates to show passing tests and we now know that in python
- `False` is not `None`
- `True` is not `None`
- `None` is `None`
- `False` is not `True`
- `False` is `False`

## AssertionError with True

Can we raise an `AssertionError` for things that are `True`?

### <span style="color:red">**RED**</span>: make it fail

update `TestAssertionError` in `test_assertion_error.py` with the following test
```python
    def test_assertion_errors_with_true(self):
        assert False is True
```
the terminal updates to show
```python
E       assert False is True
```

### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_true` to make it pass
```python
        assert True is True
```
the terminal shows passing tests

### <span style="color:red">**RED**</span>: make it fail

let's try with the above tests with the `unittest` equivalent method. update `test_assertion_errors_with_true`

```python
        self.assertTrue(False)
```
the terminal updates to show
```python
E       AssertionError: False is not true
```

### <span style="color:green">**GREEN**</span>: make it pass

we update `test_assertion_error_with_false` to make it pass
```python
        self.assertTrue(True)
```
a familiar solution. It was one of the options to solve the failing test in [TDD Setup](./TDD_SETUP.md). We also now know that in python
- `True` is not `None`
- `False` is not `None`
- `None` is `None`
- `False` is not `True`
- `False` is `False`
- `True` is not `False`
- `True` is `True`

We could sum up the above statements this way - in python `True`, `False` and `None` are different.

How does knowing these distinctions help us write useful programs? they come in handy when learning how a system behaves, they are also our python beliefs, fundamentals, truths - a foundation that gives a predictable expectation of programs written in the language.

## AssertionError with Equality

We can also make assertions of equality, where we compare if two things are equal

### <span style="color:red">**RED**</span>: make it fail

we will add a test to `TestAssertionError` in `test_assertion_errors.py`

```python
    def test_assertion_errors_with_equality(self):
        assert False == None
```

the terminal updates to show

```python
E       assert False == None
```

this `assert` statement could be translated in english as `ensure False is equal to None`

### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_equality` to make it pass

```python
        assert False != None
```
the terminal updates to show passing tests.

### <span style="color:orange">**REFACTOR**</span>: make it better

- #### <span style="color:red">**RED**</span>: make it fail
    update `test_assertion_errors_with_equality` with the `unittest` equivalent method
    ```python
            self.assertEqual(False, None)
    ```
    the `assertEqual` method checks that the 2 inputs given are equal
    does this look familiar. In [03_TYPE_ERROR](./03_TYPE_ERROR.md) we looked at function signatures. `assertEqual` is a method(function) in the `unittest.TestCase` class that according to its signature definition, when given two inputs it checks if they are equal. We could imagine that in a file named `unittest.py` there is a definition that looks like this
    ```python
    class TestCase():
        def assertEqual(positional_argument_1, positional_argument_2):
            assert positional_argument_1 == positional_argument_2
    ```

the terminal updates to show
```python
E       AssertionError: False != None
```

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_equality` to make it pass

```python
    self.assertNotEqual(False, None)
```

the terminal updates to show passing tests and we now know that in python
- `False` is not `None` and `False` is not equal to `None`
- `True` is not `None`
- `None` is `None`
- `False` is not `True`
- `False` is `False`
- `True` is not `False`
- `True` is `True`

#### <span style="color:red">**RED**</span>: make it fail

update `test_assertion_errors_with_equality`
```python
        assert True == None
```
the terminal updates to show
```python
E       assert True == None
```

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_equality` to make it pass

```python
        assert True != None
```
the terminal updates to show passing tests

#### <span style="color:red">**RED**</span>: make it fail

update `test_assertion_errors_with_equality` using the equivalent `unittest` method

```python
        self.assertEqual(True, None)
```
the terminal updates to show
```python
E       AssertionError: True != None
```

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_equality` to make it pass

```python
        self.assertNotEqual(True, None)
```
the terminal updates to show passing tests and we now know that in python
- `False` is not `None` and `False` is not equal to `None`
- `True` is not `None` and `True` is not equal to `None`
- `None` is `None`
- `False` is not `True`
- `False` is `False`
- `True` is not `False`
- `True` is `True`

#### <span style="color:orange">**REFACTOR**</span>: make it better

There is a pattern here, let's update the test for the other cases we have

#### <span style="color:red">**RED**</span>: make it fail

update `test_assertion_errors_with_equality`

```python
        assert False == True
        self.assertEqual(False, True)

        assert False != False
        self.assertNotEqual(False, False)

        assert None != None
        self.assertNotEqual(None, None)

        assert True == False
        self.assertEqual(True, False)

        assert True != True
        self.assertNotEqual(True, True)
```

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_equality` to make it pass. Once all the tests pass we can conclude that in python
- `False` is not `None` and `False` is not equal to `None`
- `True` is not `None` and `True` is not equal to `None`
- `None` is `None` and `None` is equal to `None`
- `False` is not `True` and `False` is not equal to `True`
- `False` is `False` and `False` is equal to `False`
- `True` is not `False` and `True` is not equal to `False`
- `True` is `True` and `True` is equal to `True`

***FOOD FOR THOUGHT***
> do these statements mean the following
> - when x is y, x is also equal to y?
> - when x is not y, x is also not equal to y?

***WELL DONE***
You now know How to
- test for equality
- test if something is `None` or not
- test if something is `False` or not
- test if something is `True` or not
- use `assert` statements
- use `unittest`
  - `self.assertIsNone`     - is this thing `None`?
  - `self.assertIsNotNone`
  - `self.assertFalse`      - is this thing `False`?
  - `self.assertTrue`       - is this thing `True`?
  - `self.assertEqual`      - are these two things equal?
  - `self.assertNotEqual`   - are these two things unequal?

Do you want to [read more about unittest.TestCase methods](https://docs.python.org/3/library/unittest.html?highlight=unittest#classes-and-functions)?