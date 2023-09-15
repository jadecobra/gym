# AssertionError

In this chapter we will get familiar with the [AssertionError](https://docs.python.org/3/library/exceptions.html?highlight=assertionerror#AssertionError) in python using Test Driven Development

### Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## What is an Assertion?

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

When building a program we have certain expectations based on given inputs. To test these expectations we can add `assert` statements to the program or place them in tests.

These tests help catch bugs that break previous tested behavior when introduced.

We are constantly asking these questions as we test
- What is similar?
- What is different?

The difference give us a clue as to what changes to make for our expectations and reality to match.

## AssertionError with None

### <span style="color:red">**RED**</span>: make it fail

let us create a file in the `tests` folder named `test_assertion_error.py` and add the following test using the python `assert` keyword to become familiar with the `AssertionError`

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

This `AssertionError` is triggered by the line `assert False is None`, which is similar to the question "is `False` the same as `None`?"

The difference here is that the `assert` at the beginning of the line makes the statement more like "DO NOT PROCEED UNLESS `False` is `None`"

Since `None` and `False` are different objects and are not equal, python raises an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

we update `test_assertion_errors_with_none` in `test_assertion_error.py`

```python
        assert False is not None
```

and the terminal shows passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

We can also use `assert` methods from the `unittest.TestCase` class to make assertions

- ##### <span style="color:red">**RED**</span>: make it fail
    let's add the following line to `test_assertion_errors_with_none` using the `unittest.TestCase.assertIsNone` method
    ```python
            self.assertIsNone(False)
    ```
    the terminal updates to show a similar, though more descriptive error
    ```python
    E       AssertionError: False is not None

    tests/test_assertion_error.py:8: AssertionError
    ```
    since `False is not None` we get an `AssertionError`

- #### <span style="color:green">**GREEN**</span>: make it pass
    when we update the assert statement to
    ```python
            self.assertIsNotNone(False)
    ```
    the terminal shows passing tests because this `assert` statement is `True`, which tells us that in python `False` is not `None`
- #### <span style="color:red">**RED**</span>: make it fail
    we add another test to `test_assertion_errors_with_none` to find out the relation of `None` to `True`
    ```python
            assert True is None
    ```
    and the terminal updates to show an `AssertionError`
    ```python
    E       assert True is None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    when we update the failing line in `test_assertion_errors_with_none` to
    ```python
            assert True is not None
    ```
    the terminal shows passing tests
- #### <span style="color:red">**RED**</span>: make it fail
    let's add a variation of the above statement using the `unittest.TestCase` equivalent method in `test_assertion_errors_with_none`
    ```python
            self.assertIsNone(True)
    ```
    and the terminal updates to show
    ```python
    E       AssertionError: True is not None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_none` to make it pass
    ```python
            self.assertIsNotNone(True)
    ```
    since the terminal shows passing tests, we can conclude that in python
    - `True` is not `None`
    - `False` is not `None`
- #### <span style="color:red">**RED**</span>: make it fail
    let's add another test to `test_assertion_errors_with_none`
    ```python
            assert None is not None
    ```
    and the terminal updates to show
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
    add another test to `test_assertion_errors_with_none` using the `unittest.TestCase` method
    ```python
            self.assertIsNotNone(None)
    ```
    and the terminal updates to show
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
    - `None` is `None`
    - `True` is not `None`
    - `False` is not `None`

Which of the `assert` statements do you prefer when testing `None`?
- `assert x is None`
- `self.assertIsNone(x)`

## AssertionError with False

Going with what we know so far, can we raise an `AssertionError` for things that are `False`?

### <span style="color:red">**RED**</span>: make it fail

let's update `TestAssertionError` in `test_assertion_error.py` with the following test to find out

```python
    def test_assertion_errors_with_false(self):
        assert True is False
```

the terminal updates to show
```python
E       assert True is False
```
### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_errors_with_false`
```python
        assert False is False
```
and the terminal updates to show passing tests

### <span style="color:red">**RED**</span>: make it fail
let's try the same test with the equivalent `unittest` method by updating `test_assertion_errors_with_false` with

```python
        self.assertFalse(True)
```
the terminal updates to show a failure
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
- `False` is `False`
- `False` is not `True`
- `None` is `None`
- `True` is not `None`
- `False` is not `None`

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

let's try the above test with the `unittest.TestCase` equivalent method, update `test_assertion_errors_with_true`

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
This was one of the options to solve the failing test in [TDD Setup](./TDD_SETUP.md). Our knowledge of python has grown, we now know that
- `True` is `True`
- `True` is not `False`
- `False` is `False`
- `False` is not `True`
- `None` is `None`
- `True` is not `None`
- `False` is not `None`

We could sum up the above statements this way - in python `True`, `False` and `None` are different.

Knowing these distinctions can help us write useful programs as they come in handy when learning how a system behaves, they are now our python beliefs, fundamentals, truths - a foundation that is a predictable expectation of the language.

## AssertionError with Equality

We can also make assertions of equality, where we compare if two things are the same

### <span style="color:red">**RED**</span>: make it fail

we add a test to `TestAssertionError` in `test_assertion_errors.py`

```python
    def test_assertion_errors_with_equality(self):
        assert False == None
```

and the terminal updates to show

```python
E       assert False == None
```

this `assert` statement could be translated in english as `ensure False is equal to None`

### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_equality` to make it pass

```python
        assert False != None
```
the terminal updates to show passing tests because `False` is not equal to `None`

### <span style="color:orange">**REFACTOR**</span>: make it better

- #### <span style="color:red">**RED**</span>: make it fail
    update `test_assertion_errors_with_equality` with the `unittest` equivalent method
    ```python
            self.assertEqual(False, None)
    ```
    the terminal updates to show
    ```python
    E       AssertionError: False != None
    ```
    the `assertEqual` method from `unittest.TestCase` checks if the 2 given inputs - `False` and `None` in this case - are equal. In [TypeError](./TYPE_ERROR.md) we look at function signatures to get a better understanding of providing inputs to functions.

    For our learning purpose, we could imagine that in a file named `unittest.py` there is a definition that means something like the code below. We could also [look at the real definition of the assertEqual method](https://github.com/python/cpython/blob/f1f85a42eafd31720cf905c5407ca3e043946698/Lib/unittest/case.py#L868)
    ```python
    class TestCase(object):
        def assertEqual(self, positional_argument_1, positional_argument_2):
            assert positional_argument_1 == positional_argument_2
    ```

- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_equality` to make it pass

    ```python
        self.assertNotEqual(False, None)
    ```
    the terminal updates to show passing tests

    We now know that in python
    - `True` is `True`
    - `True` is not `False`
    - `False` is `False`
    - `False` is not `True`
    - `None` is `None`
    - `True` is not `None`
    - `False` is not `None` and `False` is not equal to `None`

- #### <span style="color:red">**RED**</span>: make it fail
    update `test_assertion_errors_with_equality`
    ```python
            assert True == None
    ```
    the terminal updates to show
    ```python
    E       assert True == None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_equality` to make it pass
    ```python
            assert True != None
    ```
- #### <span style="color:red">**RED**</span>: make it fail
    update `test_assertion_errors_with_equality` using the equivalent `unittest` method
    ```python
            self.assertEqual(True, None)
    ```
    the terminal updates to show
    ```python
    E       AssertionError: True != None
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_equality` to make it pass
    ```python
            self.assertNotEqual(True, None)
    ```
    the terminal updates to show passing tests and we can update what we know about python to say
    - `True` is `True`
    - `True` is not `False`
    - `False` is `False`
    - `False` is not `True`
    - `None` is `None`
    - `True` is not `None` and `True` is not equal to `None`
    - `False` is not `None` and `False` is not equal to `None`

There is a pattern here, let's update the test with the other cases from our statement above
- #### <span style="color:red">**RED**</span>: make it fail
    update `test_assertion_errors_with_equality`

    ```python
            assert True != True
            self.assertNotEqual(True, True)

            assert True == False
            self.assertEqual(True, False)

            assert False != False
            self.assertNotEqual(False, False)

            assert False == True
            self.assertEqual(False, True)

            assert None != None
            self.assertNotEqual(None, None)
    ```
- #### <span style="color:green">**GREEN**</span>: make it pass
    update `test_assertion_errors_with_equality` to make it pass. Once all the tests pass we can conclude that in python
    - `True` is `True` and `True` is equal to `True`
    - `True` is not `False` and `True` is not equal to `False`
    - `False` is `False` and `False` is equal to `False`
    - `False` is not `True` and `False` is not equal to `True`
    - `None` is `None` and `None` is equal to `None`
    - `True` is not `None` and `True` is not equal to `None`
    - `False` is not `None` and `False` is not equal to `None`

***WELL DONE!*** Your magic powers are growing. You now know
- how to test for equality
- how to test if something is `None` or not
- how to test if something is `False` or not
- how to test if something is `True` or not
- how to use `assert` statements
- how to use the following `unittest.TestCase.assert` methods
  - `assertIsNone`     - is this thing `None`?
  - `assertIsNotNone`  - is this thing not `None`?
  - `assertFalse`      - is this thing `False`?
  - `assertTrue`       - is this thing `True`?
  - `assertEqual`      - are these two things equal?
  - `assertNotEqual`   - are these two things not equal?

Do you want to [read more about unittest.TestCase methods](https://docs.python.org/3/library/unittest.html?highlight=unittest#classes-and-functions)?

> ***FOOD FOR THOUGHT***
> - when x is y, is x also equal to y?
> - when x is not y, is x also not equal to y?
