# How to solve the AssertionError in python

We will step through solving an `AssertionError` in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## What is an Assertion?

Is it a statement of fact? Is it a belief?
Is it some fundamental thing that we agree upon?

In python an `AssertionError` is raised when the result of an `assert` statement is `False`. We are familiar with an `assert` statement from the first failing test we wrote

```python
self.assertFalse(True)
```

which is another way of saying

```python
assert False is True
```

## Why are asserts important?

When building a program we have certain expectations based on given inputs. One way to test these expectations is by adding assert statements in the program, another is by using assert statements in the tests to check whether our expectations match reality. It helps us check that the system is doing what it was designed to do, and also catch things that break previous behavior when introduced.

## How to solve the AssertionError

### <span style="color:red">**RED**</span>: make it fail

create a file named `test_assertion_error.py` in the `tests` folder and add the following

```python
import unittest


class TestAssertionError(unittest.TestCase):

    def test_assertion_errors_with_none(self):
        assert None is False        # this uses the python assert keyword
```

the terminal updates to show

```python
E       assert None is False

tests/test_assertion_error.py:7: AssertionError
```

- This error is triggered by the line `assert None is False` which is like asking the question "is `None` the same as `False`?"
- The difference here is that the `assert` of the beginning of the line makes the statement more like "Make sure `None` is the same as `False`"
- Since In python `None` is not `False`, python raises an `AssertionError`

### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_none` in `test_assertion_error.py` to make it pass

```python
        assert None is not False
```

the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

What is another way we can write `assert` statements?

##### <span style="color:red">**RED**</span>: make it fail

add the following line to `test_assertion_errors_with_none`

```python
        self.assertIsNone(False)    # this uses the unittest.TestCase assertIsNotNone method
```

the terminal updates to show a more descriptive error

```python
E       AssertionError: False is not None

tests/test_assertion_error.py:8: AssertionError
```

- since `False is not None` we get an AssertionError

#### <span style="color:green">**GREEN**</span>: make it pass

update the assert statement to make it pass

```python
        self.assertIsNotNone(False)
```

the terminal updates to show passing tests because we have an `assert` statement that is `True`.
As we learned earlier `False` is not `None`.

From our test we now know that In python
- `False` is not `None`

If `False` is not `None`, what is its relation to `True`?
Let's add a test to find out

#### <span style="color:red">**RED**</span>: make it fail

update `test_assertion_errors_with_none`
```python
        assert None is True
```
the terminal updates to show
```python
E       assert None is True
```

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_none` to make it pass
```python
        assert None is not True
```
the terminal shows passing tests

##### <span style="color:red">**RED**</span>: make it fail

let's try with the `unittest` equivalent method. update `test_assertion_errors_with_none`
```python
        self.assertIsNone(True)
```
the terminal updates to show
```python
E       AssertionError: True is not None
```

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_none` to make it pass
```python
        self.assertIsNotNone(True)
```
the terminal shows passing tests and We now know that in python
- `False` is not `None`
- `True` is not `None`

What else can we discover? How can we use this fundamental information to build programs?

#### <span style="color:red">**RED**</span>: make it fail

Let's add another test. Update `test_assertion_errors_with_none`
```python
        assert None is not None
```
The terminal updates to show
```python
E       assert None is not None
```

#### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_errors_with_none` to make it pass
```python
        assert None is None
```
the terminal updates to show passing tests. Let's add more

##### <span style="color:red">**RED**</span>: make it fail
update `test_assertion_errors_with_none`
```python
        self.assertIsNotNone(None)
```
the terminal updates to show
```python
>       self.assertIsNotNone(None)
E       AssertionError: unexpectedly None
```

#### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_errors_with_none` to make it pass
```python
        self.assertIsNone(None)
```
the terminal updates to show passing tests and we now know that in python
- `False` is not `None`
- `True` is not `None`
- `None` is `None`

Which do you prefer for testing `None`?
- `assert x is None`        - this can be used anywhere
- `self.assertIsNone(x)`    - this can only be used in a `unittest.TestCase`

What else can we learn with what we know?
- Can we raise an `AssertionError` for things that are `False`
- Can we raise an `AssertionError` for things that are `True`

Let's test it

#### <span style="color:red">**RED**</span>: make it fail

update `TestAssertionError` in `test_assertion_error.py` with the following test
```python
    def test_assertion_errors_with_false(self):
        assert False is True
```
the terminal updates to show
```python
E       assert False is True
```

#### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_errors_with_false` to make it pass
```python
        assert False is False
```
the terminal updates to show passing tests

#### <span style="color:red">**RED**</span>: make it fail
let's try with the `unittest` equivalent method. update `test_assertion_errors_with_false`

```python
        self.assertFalse(True)
```
the terminal updates to show
```python
E       AssertionError: True is not false
```
a familiar test, this was the test that started us on the journey of test driven development in python.

#### <span style="color:green">**GREEN**</span>: make it pass
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

#### <span style="color:red">**RED**</span>: make it fail

update `TestAssertionError` in `test_assertion_error.py` with the following test
```python
    def test_assertion_errors_with_true(self):
        assert True is False
```
the terminal updates to show
```python
E       assert True is False
```

#### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_errors_with_true` to make it pass
```python
        assert True is True
```
the terminal updates to show passing tests

#### <span style="color:red">**RED**</span>: make it fail
let's try with the `unittest` equivalent method. update `test_assertion_errors_with_true`

```python
        self.assertTrue(False)
```
the terminal updates to show
```python
E       AssertionError: False is not true
```

#### <span style="color:green">**GREEN**</span>: make it pass
update `test_assertion_error_with_false` to make it pass
```python
        self.assertTrue(True)
```
a familiar solution. This was an option to solve the failing test that started us on the journey of test driven development in python.
the terminal updates to show passing tests

the terminal updates to show passing tests and we now know that in python
- `False` is not `None`
- `True` is not `None`
- `None` is `None`
- `False` is not `True`
- `False` is `False`
- `True` is not `False`
- `True` is `True`

We could sum it up that so far we know that in python `True`, `False` and `None` are different.

How does this help us write programs? Why do we care about these distinctions?
Well, they come in handy when we are learning how a system behaves, they are also our python beliefs/fundamentals/truths, giving us a predictable expectation of programs written in the language as they will all be following those rules.

We can also make assertions of equality. Let us test this

#### <span style="color:red">**RED**</span>: make it fail

update `TestAssertionError` in `test_assertion_errors.py` with a new test

```python
    def test_assertion_errors_with_equality(self):
        assert False == None
```
the terminal updates to show
```python
E       assert False == None
```
this test could be translated in english as `ensure False is equal to None`

#### <span style="color:green">**GREEN**</span>: make it pass

update `test_assertion_errors_with_equality` to make it pass

```python
        assert False != None
```
the terminal updates to show passing tests.

#### <span style="color:orange">**REFACTOR**</span>: make it better

##### <span style="color:red">**RED**</span>: make it fail
update `test_assertion_errors_with_equality` with the `unittest` equivalent method

```python
        self.assertEqual(False, None)
```
- this method checks that the 2 inputs given are equal
- does this look familiar. In [03_TYPE_ERROR](./03_TYPE_ERROR.md) we looked at function signatures. `assertEqual` is a method(function) in the `unittest.TestCase` class that according to its signature definition, when given two inputs it checks if they are equal. We could imagine that in a file named `unittest.py` there is a definition that looks like this
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