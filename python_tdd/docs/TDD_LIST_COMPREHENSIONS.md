# List Comprehensions

We will cover `list comprehensions` in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## List Comprehension

## Creating a List with an Iterable

List comprehensions are a way to create lists from another iterable. It is a nice way to loop over elements

### <span style="color:red">**RED**</span>: make it fail

add `test_list_comprehension.py` to the `tests` folder

```python
import unittest


class TestListComprehensions(unittest.TestCase):

    def test_creating_a_list_from_an_iterable(self):
        collection_a = range(10)
        list_a = []
        self.assertEqual(list_a, [])

        for element in collection_a:
            list_a.append(element)
        self.assertEqual(list_a, [])
```
- we create `collection_a` which uses the `range` object
- what is the `range` object? it creates an `iterable` of numbers from 0 to the number we give minus 1. [read more](https://docs.python.org/3/library/stdtypes.html?highlight=range#range)
- we create a list named `list_a` that has no elements and confirm it is empty with an `assertEqual`
- we then create a loop using the `for` keyword, that goes over every element of `collection_a` and adds it to `list_a` using the `append` method we learned in [TDD_LISTS](./TDD_LISTS.md)
- the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for our  test to check the elements of `list_a` after the loop runs
    ```python
    E       AssertionError: Lists differ: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] != []
    E
    E       First list contains 10 additional elements.
    E       First extra element 0:
    E       0
    E
    E       - [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    E       + []
    ```

### <span style="color:green">**GREEN**</span>: make it pass

update the tests with the expected value

```python
    def test_creating_a_list_from_an_iterable(self):
        collection_a = range(10)
        list_a = []
        self.assertEqual(list_a, [])

        for element in collection_a:
            list_a.append(element)
        self.assertEqual(list_a, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
```

the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

- add a test to check what happens when we call the `list` keyword on `collection_a`
    ```python
        self.assertEqual(list(collection_a), list_a)
    ```
    the tests pass because calling `list` on an `iterable` creates a `list`
- add another test
    ```python
        self.assertEqual(list_comprehensions.make_a_list(collection_a), list_a)
    ```
    the terminal updates to show a `NameError`
- add an import statement for `list_comprehensions` at the beginning of `test_list_comprehension.py`
    ```python
    import list_comprehensions
    import unittest
    ```
    the terminal updates to show a [ModuleNotFoundError](./00_MODULE_NOT_FOUND_ERROR.md)
- create `list_comprehensions.py` in the project folder and the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- update `list_comprehensions.py` with a function
    ```python
    def make_a_list():
        return None
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md)
- we update the signature of the function to take in an argument
    ```python
    def make_a_list(argument):
        return None
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the function to return a list of whatever argument it gets
    ```python
    def make_a_list(argument):
        return list(argument)
    ```
    the tests pass

## Creating a List with a For Loop

Let's test creating a list with a for loop like the example above

### <span style="color:red">**RED**</span>: make it fail

add a test to `TestListComprehensions`

```python
def test_creating_a_list_with_a_for_loop(self):
    collection = range(10)
    a_list = []
    self.assertEqual(a_list, [])

    for element in collection:
        a_list.append(element)

    self.assertEqual(a_list, [])
    self.assertEqual(list_comprehensions.for_loop(collection), a_list)
```

the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the values of `a_list` after we loop through `collection` and add elements

### <span style="color:green">**GREEN**</span>: make it pass

- update the right side of the test with the expected values
    ```python
    def test_creating_a_list_with_a_for_loop(self):
        collection = range(10)
        a_list = []
        self.assertEqual(a_list, [])

        for element in collection:
            a_list.append(element)

        self.assertEqual(a_list, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(list_comprehensions.for_loop(collection), a_list)
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md) since `list_comprehensions.py` does not have a definition for `for_loop`
- add a function definition to `list_comprehensions.py`
    ```python
    def for_loop():
        return None
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md)
- 
### <span style="color:orange">**REFACTOR**</span>: make it better