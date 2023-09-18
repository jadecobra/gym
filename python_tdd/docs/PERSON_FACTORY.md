# How to use dictionaries as Factories in python

We will step through creating a Person Factory in python using Test Driven Development

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Person Factory

This is an exercise in creating dictionaries using functions. It assumes you are familiar with [Functions](./FUNCTIONS.md) and [Dictionaries](./DICTIONARIES.md), We are going to attempt it even if you are not

### <span style="color:red">**RED**</span>: make it fail

create a file named `test_person_factory.py` in the `tests` folder and add the following

```python
import unittest
import person


class TestPersonFactory(unittest.TestCase):

    def test_person_factory(self):
        self.assertEqual(person.factory(), None)
```

the terminal updates to show a `ModuleNotFoundError`

### <span style="color:green">**GREEN**</span>: make it pass

- create a file named `person.py`, the terminal updates to show an [AttributeError](./ATTRIBUTE_ERROR.md)
- create a function named `factory`, the terminal updates to show passing tests
    ```python
    def factory():
        return None
    ```

### <span style="color:orange">**REFACTOR**</span>: make it better

- update `test_person_factory` with details
    ```python
    def test_person_factory(self):
        self.assertEqual(
            person.factory(
                first_name="sibling",
                last_name="last_name",
                year_of_birth=this_year(),
                sex="F"
            ),
            {
                "first_name": "sibling",
                "last_name": "last_name",
                "sex": "F",
                "age": this_year() - this_year()
            }
        )
    ```
    the terminal updates to show a `NameError` for `this_year`
- let's add a definition for it to the top of `test_person_factory.py`
    ```python
    import unittest
    import person

    def this_year():
        return None
    ...
    ```
    the terminal updates to show a [TypeError](./TYPE_ERROR.md) since our function signature does not yet accept arguments
- add a keyword argument for `first_name` to the `factory` function
    ```python
    def factory(first_name=None):
        return None
    ```
    the terminal updates to show a [TypeError](./TYPE_ERROR.md) for the next keyword argument
- add a keyword argument for `last_name`  to the `factory` function
    ```python
    def factory(first_name=None, last_name=None):
        return None
    ```
    the terminal updates to show a [TypeError](./TYPE_ERROR.md) for the next keyword argument
- we update the `factory` function definition for each keyword until we get a [TypeError](./TYPE_ERROR.md) for the line where we subtract `this_year() - this_year()` because we cannot perform a subtraction operation on `None` and our `this_year` function currently returns `None`. Let's update our definition using a function from the [datetime](https://docs.python.org/3/library/datetime.html?highlight=datetime#module-datetime) library that returns the current year we are in
    ```python
    import unittest
    import person
    import datetime

    def this_year():
        return datetime.datetime.now().year
    ```
    - we import the `datetime` library so we can use its `methods` and `attributes`
    - we return the `year` attribute of the object returned by the `now` method which is a representation of the current local date and time, we could also use `today` or `utcnow` to achieve the same thing
    - we get the `year` attribute of the object returned since that is all we are interested in
- the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) since our `factory` function returns `None` and the test expects a [dictionary](./DICTIONARIES.md). Let's update the function to return an empty dictionary
    ```python
    def factory(first_name=None, last_name=None, year_of_birth=None, sex=None):
        return {}
    ```
    the terminal updates to show the difference between the [dictionary](./DICTIONARIES.md) returned by the `factory` function and the one expected in the test
- we update the empty `dictionary` in the `factory` function to match the expected results
    ```python
    def factory(first_name=None, last_name=None, year_of_birth=None, sex=None):
        return {
            "age": 0,
            "first_name": "sibling",
            "last_name": "last_name",
            "sex": "F",
        }
    ```
    ***LOVELY!*** the tests pass! There's one problem with this function. It is going to return the exact same thing every time, regardless of what information is given to it, to make it more useful we need it to be able to use the inputs given.
- Let's add another test with a different set of inputs
    ```python
    def test_person_factory_takes_in_variable_inputs(self):
        self.assertEqual(
            person.factory(
                first_name="me",
                last_name="last_name",
                year_of_birth=1983,
                sex="M",
            ),
            {
                "first_name": "me",
                "last_name": "last_name",
                "sex": "M",
                "age": this_year() - 1983
            }
        )
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) because the expected and returned dictionaries are different
- update the `factory` function to use the input provided for first_name
    ```python
    def factory(first_name=None, last_name=None, year_of_birth=None, sex=None):
        return {
            'age': 0,
            'first_name': first_name,
            'last_name': 'last_name',
            'sex': 'F',
        }
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) but it no longer shows a difference for `first_name`. Good, let's repeat it step by step for every other input until the only error left is for the age
- we need to calculate the age. We have a function that returns the current year and we have the `year_of_birth` as an input, we also have this line in the test `this_year() - 1983`. Since `1983` is the `year_of_birth` in this case let's update the `factory` function to use that calculation
    ```python
    def factory(first_name=None, last_name=None, year_of_birth=None, sex=None):
        return {
            'age': this_year() - year_of_birth,
            'first_name': first_name,
            'last_name': last_name,
            'sex': sex,
        }
    ```
    the terminal updates to show a `NameError` since we are calling a function that does not exist in `person.py`
- replace `this_year()` with the return value from `test_person.this_year` and add an import statement
    ```python
    import datetime

    def factory(first_name=None, last_name=None, year_of_birth=None, sex=None):
        return {
            'age': datetime.datetime.now().year - year_of_birth,
            'first_name': first_name,
            'last_name': last_name,
            'sex': sex,
        }
    ```
    ***HOORAY!*** the terminal updates to show passing tests
- add another test to `test_person.py`, this time we will test default values
    ```python
    def test_person_factory_with_default_keyword_arguments(self):
        self.assertEqual(
            person.factory(
                first_name="child_a",
                year_of_birth=2014,
                sex="M",
            ),
            {
                "first_name": "child_a",
                "last_name": "last_name",
                "sex": "M",
                "age": this_year() - 2014
            }
        )
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) since the value for `last_name` does not match the expected value
- since we now have 3 tests with the same value for `last_name` we could use that value as the default value in the absence of any other examples. modify the default value for the parameter in `person.factory`
    ```python
    def factory(first_name=None, last_name="last_name", year_of_birth=None, sex=None):
    ```
    the terminal updates to show passing tests
- what if we try another default value, this time say for sex. add a test to `test_person_factory_with_default_keyword_arguments`
    ```python
        self.assertEqual(
            person.factory(
                first_name="person",
                year_of_birth=1900,
            ),
            {
                "first_name": "person",
                "last_name": "last_name",
                "age": this_year() - 1900,
                "sex": "M"
            }
        )
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md)
- since 3 out of our 4 persons created have `M` as their sex and 1 has `F` as their sex, we could set the majority to the default to reduce the number of repetitions. modify the default value for the parameter in `person.factory`
    ```python
    def factory(first_name=None, last_name="last_name", year_of_birth=None, sex='M'):
    ```
    the terminal updates to show passing tests

***CONGRATULATIONS***
You know how to define
- functions with keyword arguments with defaults
- dictionaries