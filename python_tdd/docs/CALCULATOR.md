# How to create a Calculator using Test Driven Development

We will step through creating a calculator using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Environment](./TDD_SETUP.md)

---

## Add Tests

Update `test_calculator.py` with a TODO list to keep track of what needs to be done
```python
import unittest


class TestCalculator(unittest.TestCase):

    def test_failure(self):
        self.assertTrue(True)

# TODO
# test importing
# test addition
# test subtraction
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
```

the terminal should respond since a change was made

```shell
=============== 1 passed in 0.01s ===========================

Change detected: tests/test_calculator.py

[TODAYS_DATE] Running: py.test
===================== test session starts ===================
platform <YOUR_OPERATING_SYSTEM> -- python <YOUR_python_VERSION>, pytest-<VERSION>, pluggy-<VERSION>
rootdir: <YOUR_PATH>/calculator
collected 1 item

tests/test_calculator.py .                                                                                                    [100%]

==================== 1 passed in 0.00s =====================
```

### Add the import test

```python
import unittest
import calculator


class TestCalculator(unittest.TestCase):

    def test_failure(self):
        self.assertTrue(True)

# TODO
# test importing
# test addition
# test subtraction
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
```

- `import calculator` - imports the calculator module we are writing/testing

### Test Addition

#### <span style="color:red">**RED**</span>: make it fail

```python
import unittest
import calculator


class TestCalculator(unittest.TestCase):

    def test_failure(self):
        self.assertTrue(True)

    def test_addition(self):
        self.assertEqual(
            calculator.add(0, 1),
            1
        )

# TODO
# test addition
# test subtraction
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
```

- remove `test import` from the TODO list since it passed and the task is completed
- add `test_addition` to the list of tests
- there's a new method `self.assertEqual` this checks if 2 things are the same it is similar to `assert x == y` or asking `is x equal to y?`
- there are two things passed to the `self.assertEqual` for evaluation
    - calculator.add(0, 1) - when we pass the values 0 and 1 to the addition function
    - 1 - we expect it to return one

    the terminal updates with the following

    ```python
    ...
    collected 2 items

    tests/test_calculator.py F.                                                                                                   [100%]

    =========================== FAILURES =======================
    ______________ TestCalculator.test_addition ________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
    >           calculator.add(0, 1),
                1
            )
    E       AttributeError: module 'calculator' has no attribute 'add'

    tests/test_calculator.py:12: AttributeError
    ============== short test summary info +=======================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - AttributeError: module 'calculator' has no attribute 'add'
    ============ 1 failed, 1 passed in 0.02s ======================
    ```

    What does this mean?
    - The error is an `AttributeError` at line 12 in `test_calculator.py`
    - [AttributeError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#AttributeError) is raised when you try to access an attribute and python cannot find it
    - `calculator.add` is similar to an address. `calculator` refers to `calculator.py` - the python module we wrote at the beginning
    - `add` refers to something in that file that currently does not exist


#### <span style="color:green">**GREEN**</span>: make it pass

- open `calculator.py` in your Interactive Development Environment(IDE) and add this
    ```python
    add = None
    ```

    the terminal will update to show a new Error

    ```python
    ================== FAILURES =============================
    ___________ TestCalculator.test_addition ________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
    >           calculator.add(0, 1),
                1
            )
    E       TypeError: 'NoneType' object is not callable

    tests/test_calculator.py:12: TypeError
    =============== short test summary info ========================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - TypeError: 'NoneType' object is not callable
    ============== 1 failed, 1 passed in 0.03s ======================
    ```

- The `AttributeError` was fixed by declaring a variable `add` in the `calculator` module, even though it is currently defined as the null value `None`
- The new error is [TypeError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#TypeError) occurs when an `object` is used in a way that it was not intended for. The `add` variable is not callable. Let's make it callable

    update `calculator.py` to
    ```python
    def add():
        return None
    ```

    the terminal will update to a different message for the TypeError

    ```python
    ===================== FAILURES ===========================
    ___________ TestCalculator.test_addition _________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
    >           calculator.add(0, 1),
                1
            )
    E       TypeError: add() takes 0 positional arguments but 2 were given

    tests/test_calculator.py:12: TypeError
    ============== short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - TypeError: add() takes 0 positional arguments but 2 were given
    ============= 1 failed, 1 passed in 0.02s ===================
    ```
- This `TypeError` indicates that the current definition of the `add` function takes in no arguments but we provided 2. update the `add` function in `calculator.py` to match the test
    ```
    def add(x, y):
        return None
    ```
    the terminal updates to a new error
    ```python
        self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
    >       self.assertEqual(
                calculator.add(0, 1),
                1
            )
    E       AssertionError: None != 1

    tests/test_calculator.py:11: AssertionError
    ================ short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - AssertionError: None != 1
    ================ 1 failed, 1 passed in 0.02s ==================
    ```
    This one is familiar. An `AssertionError` was the first error we solved in our test for failure.
    This is caused by the left side not being equal to the right side.
    Let's make them equal. update the `add` function in `calculator.py`
    ```python
    def add(x, y):
        return 1
    ```
    Eureka! The test passes
    ```python
    tests/test_calculator.py ..                                                                                                             [100%]

    ===================== 2 passed in 0.01s ======================
    ```
#### <span style="color:orange">**REFACTOR**</span>: Make it Better

Wait a minute. Is it that easy? Do we just provide the solution to make it pass? In the green phase, yes. We do whatever it takes to make the test pass even if we have to cheat.
This shows us that our test needs to be better.
What happens if our calculator users try to add other numbers?
What happens if our calculator users try to add a negative number?
Can we make it better?

- <span style="color:red">**RED**</span>: make it fail - update `test_calculator.py` with a new test
    ```python
    import unittest
    import calculator


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(0, 1),
                1
            )
            self.assertEqual(
                calculator.add(-1, 1),
                0
            )

    # TODO
    # test addition
    # test subtraction
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response

    ```python
    ======================= FAILURES =====================================
    _____________ TestCalculator.test_addition ___________________________

    self = <tests.test_calculator.TestCalculator testMethod=test_addition>

        def test_addition(self):
            self.assertEqual(
                calculator.add(0, 1),
                1
            )
    >       self.assertEqual(
                calculator.add(-1, 1),
                0
            )
    E       AssertionError: 1 != 0

    tests/test_calculator.py:15: AssertionError
    ================== short test summary info ===========================
    FAILED tests/test_calculator.py::TestCalculator::test_addition - AssertionError: 1 != 0
    ================= 1 failed, 1 passed in 0.02s ========================
    ```
    Another AssertionError
- <span style="color:green">**GREEN**</span>: make it pass - update the `add` function in `calculator.py`
    ```python
    def add(x, y):
    return x + y
    ```
    terminal response
    ```
    tests/test_calculator.py ..                      [100%]

    ====================== 2 passed in 0.01s ==============
    ```
- <span style="color:orange">**REFACTOR**</span>: Make it Better

    let's randomize the inputs to make sure the function behaves the way we expect for any integers.
    update `test_calculator.py` to use the [random](https://docs.python.org/3/library/random.html?highlight=random#module-random) library
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
                calculator.add(x, y),
                x+y
            )

    # TODO
    # test addition
    # test subtraction
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    - set a variable x to a random integer between -1 and 1
    - set a variable y to a random integer between -1 and 1
    - test that when you give these two variables to the `add` function you get a sum of the 2 variables back

    terminal response
    ```
    tests/test_calculator.py ..           [100%]

    ================ 2 passed in 0.01s ===========================
    ```
    - we no longer need the previous 2 tests because this new test covers those cases and more
    - remove `test addition` from the TODO list since it passed and the task is completed

That's the pattern <span style="color:red">**RED**</span> <span style="color:green">**GREEN**</span> <span style="color:orange">**REFACTOR**</span>

---


### Test Subtraction

Let's add the other tests
#### <span style="color:red">**RED**</span> : make it fail

- update `test_calculator.py` with `test_subtraction`
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
                calculator.add(x, y),
                x+y
            )

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
                calculator.subtract(x, y),
                x-y
            )

    # TODO
    # test subtraction
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response - AttributeError
    ```python

    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
    >           calculator.subtract(x, y),
                x-y
            )
    E       AttributeError: module 'calculator' has no attribute 'subtract'

    tests/test_calculator.py:23: AttributeError
    =============== short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - AttributeError: module 'calculator' has no attribute 'subtract'
    ============== 1 failed, 2 passed in 0.03s ==================
    ```
    update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    subtract = None
    ```
    terminal response - TypeError
    ```python
    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
    >           calculator.subtract(x, y),
                x-y
            )
    E       TypeError: 'NoneType' object is not callable

    tests/test_calculator.py:23: TypeError
    =================== short test summary info =============
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - TypeError: 'NoneType' object is not callable
    =============== 1 failed, 2 passed in 0.02s ============
    ```
    update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    def subtract():
        return None
    ```
    terminal response - TypeError
    ```python
    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            self.assertEqual(
    >           calculator.subtract(x, y),
                x-y
            )
    E       TypeError: subtract() takes 0 positional arguments but 2 were given

    tests/test_calculator.py:23: TypeError
    =================== short test summary info ============================
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - TypeError: subtract() takes 0 positional arguments but 2 were given
    =================== 1 failed, 2 passed in 0.02s =========================
    ```

#### <span style="color:green">**GREEN**</span> : make it pass

- update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    def subtract(x, y):
        return None
    ```
    terminal response - AssertionError
    ```python
    self = <tests.test_calculator.TestCalculator testMethod=test_subtraction>

        def test_subtraction(self):
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
    >       self.assertEqual(
                calculator.subtract(x, y),
                x-y
            )
    E       AssertionError: None != 0

    tests/test_calculator.py:22: AssertionError
    ================= short test summary info ===================
    FAILED tests/test_calculator.py::TestCalculator::test_subtraction - AssertionError: None != 0
    ================ 1 failed, 2 passed in 0.02s ================
    ```
    update `calculator.py`
    ```python
    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y
    ```
    terminal response - SUCCESS!
    ```shell
    collected 3 items

    tests/test_calculator.py ...                          [100%]

    ======================= 3 passed in 0.01s ==================
    ```
- remove `test subtraction` from the TODO list

#### <span style="color:orange">**REFACTOR**</span>: make it better

- How can we make this better?
- Is there any duplication that could be removed? Yes
    - `x = random.randint(-1, 1)` happens 2 times
    - `y = random.randint(-1, 1)` happens 2 times


- update `test_calculator.py`
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

    # TODO
    # test multiplication
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response stays the same
    the x and y variables are now initialized as class variables that can be referenced later using `self.x` and `self.y`

---

### Test Multiplication

#### <span style="color:red">**RED**</span> : make it fail

update `test_calculator.py` with `test_multiplication`
```python
import unittest
import calculator
import random


class TestCalculator(unittest.TestCase):

    x = random.randint(-1, 1)
    y = random.randint(-1, 1)

    def test_failure(self):
        self.assertTrue(True)

    def test_addition(self):
        self.assertEqual(
            calculator.add(self.x, self.y),
            self.x+self.y
        )

    def test_subtraction(self):
        self.assertEqual(
            calculator.subtract(self.x, self.y),
            self.x-self.y
        )

    def test_multiplication(self):
        self.assertEqual(
            calculator.multiply(self.x, self.y),
            self.x*self.y
        )

# TODO
# test multiplication
# test division

# Exceptions Encountered
# AssertionError
# AttributeError
# TypeError
```
terminal response - AttributeError

#### <span style="color:green">**GREEN**</span> : make it pass
update `calculator.py`
```python
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y
```
terminal response - SUCCESS
#### <span style="color:orange">**REFACTOR**</span>: make it better

- remove `test_multiplication` from the TODO list
- Can you think of any way to make the code better?

---

### Test Division

#### <span style="color:red">**RED**</span> : make it fail
- update `test_calculator.py` with `test_division`
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            self.assertEqual(
                calculator.divide(self.x, self.y),
                self.x/self.y
            )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    ```
    terminal response - AttributeError
- update `calculator.py` with `divide`
    ```python
    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y

    def multiply(x, y):
        return x * y

    def divide(x, y):
        return x / y
    ```
    terminal response may vary. When y is 0 we get a [ZeroDivisionError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#ZeroDivisionError)
    ```python
    x = 1, y = 0

        def divide(x, y):
    >       return x / y
    E       ZeroDivisionError: division by zero

    calculator.py:11: ZeroDivisionError
    ================= short test summary info ========================
    FAILED tests/test_calculator.py::TestCalculator::test_division - ZeroDivisionError: division by zero
    ==================== 1 failed, 4 passed in 0.03s =================
    ```
    add `ZeroDivisionError` to the list of errors encountered

##### How to test for Errors
- <span style="color:red">**RED**</span> : make it fail
    - update `test_calculator.py` with a test for division by zero
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            self.assertEqual(
                calculator.divide(self.x, 0),
                self.x/0
            )
            # self.assertEqual(
            #     calculator.divide(self.x, self.y),
            #     self.x/self.y
            # )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    # ZeroDivisionError
    ```
    terminal response
    ```python
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    x = 0, y = 0

        def divide(x, y):
    >       return x / y
    E       ZeroDivisionError: division by zero

    calculator.py:11: ZeroDivisionError
    ================= short test summary info ======================
    FAILED tests/test_calculator.py::TestCalculator::test_division - ZeroDivisionError: division by zero
    =================== 1 failed, 4 passed in 0.02s ================
    ```

- <span style="color:green">**GREEN**</span> : make it pass
    - update `test_calculator.py` to confirm that `ZeroDivisionError` is raised when dividing by 0
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            with self.assertRaises(ZeroDivisionError):
                calculator.divide(self.x, 0)
            # self.assertEqual(
            #     calculator.divide(self.x, self.y),
            #     self.x/self.y
            # )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    # ZeroDivisionError
    ```
    terminal response - SUCCESS - We now have a way to `catch` Exceptions in testing, allowing tests to continue when they encounter expected failures

- <span style="color:orange">**REFACTOR**</span>: make it better
    - update `test_calculator.py` to test other division cases when the divisor is not 0 by adding a while condition
    ```python
    import unittest
    import calculator
    import random


    class TestCalculator(unittest.TestCase):

        x = random.randint(-1, 1)
        y = random.randint(-1, 1)

        def test_failure(self):
            self.assertTrue(True)

        def test_addition(self):
            self.assertEqual(
                calculator.add(self.x, self.y),
                self.x+self.y
            )

        def test_subtraction(self):
            self.assertEqual(
                calculator.subtract(self.x, self.y),
                self.x-self.y
            )

        def test_multiplication(self):
            self.assertEqual(
                calculator.multiply(self.x, self.y),
                self.x*self.y
            )

        def test_division(self):
            with self.assertRaises(ZeroDivisionError):
                calculator.divide(self.x, 0)
            while self.y == 0:
                self.y = random.randint(-1, 1)
            self.assertEqual(
                calculator.divide(self.x, self.y),
                self.x/self.y
            )

    # TODO
    # test division

    # Exceptions Encountered
    # AssertionError
    # AttributeError
    # TypeError
    # ZeroDivisionError
    ```
    - `while self.y == 0:` this creates a loop, you are telling python to repeat the block that follows as long as `self.y is equal to 0`
    - remove `test_division` from `TODO`

---

***CONGRATULATIONS*** You made it through writing a program that can perform the 4 basic arithmetic operations using Test Driven Development
