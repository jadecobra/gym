# Lists

We will cover `lists/arrays` in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Data Structures

In programming we process input data of some form and output data in some form.
We can think of it as

```python
input_data -> program -> output_data
f(input_data) -> output_data # where f is the program|procress
```

## What are the data structures in python

- `None` - none - no value
- `bool` - boolean - True | False
- `int` - integers - positive/negative whole numbers e.g. -1, 0, 1
- `float` - floats - floating point numbers e.g. -1.1, 0.1, 1.1
- `str` - string - any text in strings"
- `tuple` - tuples - an immutable sequence of values
- `list` - lists | arrays - a mutable sequence of values
- `set` - sets - a sequence of values with no duplicates
- `dict` - dictionaries - a mapping of key, values

## What is a list/array?

A `list` is an object that holds elements. It is a container like `tuples` and `sets`.
In python
- Lists are represented with `[]`
- Lists can also be created with the `list` keyword
- Lists are mutable which means they can be changed after creation, tuples are not, they are immutable


Let's play with lists

## How to create a list

### <span style="color:red">**RED**</span>: make it fail

add a file named `test_lists.py` to the `tests` folder

```python
import unittest


class TestLists(unittest.TestCase):

    def test_creating_list_with_list_keyword(self):
        self.assertEqual(list(0, 1, 2, 3), [])
```
the terminal shows a [TypeError](./03_TYPE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- Looking at the error we see that the `list` keyword expects one argument but we gave it four, so we are violating the signature for creating lists. How can we pass in values correctly to this object?
- We check out the [documentation](https://docs.python.org/3/library/stdtypes.html?highlight=list#list) and see that list takes in an `iterable`
- What is an iterable? any object that we can loop over
- update the left value in the test
    ```python
    def test_creating_list_with_list_keyword(self):
        self.assertEqual(list((0, 1, 2, 3)), [])
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
    ```python
    >       self.assertEqual(list((0, 1, 2, 3)), [])
    E       AssertionError: Lists differ: [0, 1, 2, 3] != []
    E
    E       First list contains 4 additional elements.
    E       First extra element 0:
    E       1
    E
    E       - [0, 1, 2, 3]
    E       + []
    ```
- update the right side to match the values on the left from the terminal
    ```python
    def test_creating_list_with_list_keyword(self):
        self.assertEqual(list((0, 1, 2, 3)), [0, 1, 2, 3])
    ```
    the test passes

### <span style="color:orange">**REFACTOR**</span>: make it better

- we know we can create a list with the `list` keyword but our passing test also shows we can create a list with `[]` and it uses less characters. Let's test it, add a test
    ```python
    def test_creating_list_with_square_brackets(self):
        self.assertEqual([0, 1, 2, 3], list((0, 1, 2, 3)))
    ```

## How to add items to a list

### <span style="color:red">**RED**</span>: make it fail

add a test to `TestLists` in `test_lists.py`

```python
    def test_adding_an_item_to_a_list(self):
        a_list = [0, 1, 2, 3]
        self.assertEqual(a_list, [0, 1, 2, 3])
        a_list.append(4)
        self.assertEqual(a_list, [0, 1, 2, 3])
```

the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) because after we call `a_list.append(5)`, the values in `a_list` change

```python
>       self.assertEqual(a_list, [0, 1, 2, 3])
E       AssertionError: Lists differ: [0, 1, 2, 3, 4] != [0, 1, 2, 3]
E
E       First list contains 1 additional elements.
E       First extra element 4:
E       4
E
E       - [0, 1, 2, 3, 4]
E       ?            ---
E
E       + [0, 1, 2, 3]
```

### <span style="color:green">**GREEN**</span>: make it pass

update the values on the right side of the `assertEqual` to make it match the expectation
```python
    def test_adding_an_item_to_a_list(self):
        a_list = [0, 1, 2, 3]
        self.assertEqual(a_list, [0, 1, 2, 3])
        a_list.append(4)
        self.assertEqual(a_list, [0, 1, 2, 3, 4])
```
the terminal updates to show passing tests
- we started with a list that contained 4 elements
- we added an element
- our test confirms that the element we added is the extra element in the list

## How to remove an item from a list


### <span style="color:red">**RED**</span>: make it fail

add a test to `TestLists`

```python
    def test_removing_any_item_from_a_list(self):
        a_list = [0, 1, 2, 3]
        self.assertEqual(a_list, [0, 1, 2, 3])
        a_list.remove(2)
        self.assertEqual(a_list, [0, 1, 2, 3])
```

the terminal updates to show a difference after we call `a_list.remove(2)`, because the call removes an element from `a_list`
```python
>       self.assertEqual(a_list, [0, 1, 2, 3])
E       AssertionError: Lists differ: [0, 1, 3] != [0, 1, 2, 3]
E
E       First differing element 2:
E       3
E       2
E
E       Second list contains 1 additional elements.
E       First extra element 3:
E       3
E
E       - [0, 1, 3]
E       + [0, 1, 2, 3]
E       ?
```

### <span style="color:green">**GREEN**</span>: make it pass

update the test to make the values on the right match the expected value

```python
    def test_removing_any_item_from_a_list(self):
        a_list = [0, 1, 2, 3]
        self.assertEqual(a_list, [0, 1, 2, 3])
        a_list.remove(2)
        self.assertEqual(a_list, [0, 1, 3])
```

we are green. tests are passing

### <span style="color:orange">**REFACTOR**</span>: make it better

What if there was more than one element, how does python decide which to remove when we call `.remove(element)` on a list?
Let's find out

- add a failing test
    ```python
    def test_removing_an_item_from_a_list_when_multiple_exist(self):
        a_list = [0, 2, 1, 2, 3, 2]
        self.assertEqual(a_list, [0, 2, 1, 2, 3, 2])
        a_list.remove(2)
        self.assertEqual(a_list, [0, 2, 1, 2, 3, 2])
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the  values on the right to match the expectation
    ```python
    def test_remove_an_item_from_a_list_when_multiple_exist(self):
        a_list = [0, 2, 1, 2, 3, 2]
        self.assertEqual(a_list, [0, 2, 1, 2, 3, 2])
        a_list.remove(2)
        self.assertEqual(a_list, [0, 1, 2, 3, 2])
    ```
    the tests pass. We can conclude from our experiment that the `remove` function removes the first occurrence of an item from a list
