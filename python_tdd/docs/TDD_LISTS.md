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

## How to remove the last item in a list

### <span style="color:red">**RED**</span>: make it fail

add a test to `TestLists` in `test_lists.py`

```python
    def test_removing_the_last_item_of_a_list(self):
        a_list = [0, 1, 2, 3]
        self.assertEqual(a_list, [0, 1, 2, 3])
        last_item = a_list.pop()
        self.assertEqual(last_item, 0)
        self.assertEqual(a_list, [0, 1, 2, 3])
```
- we define a list as containing 4 elements and confirm the values
- we call the `pop` function, then check the value that gets popped
- we check the list to see what values remain after calling `pop`

the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the test that checks the value of the item that is popped

### <span style="color:green">**GREEN**</span>: make it pass

- update the value to match the actual value popped
    ```python
    def test_removing_the_last_item_of_a_list(self):
        a_list = [0, 1, 2, 3]
        self.assertEqual(a_list, [0, 1, 2, 3])
        last_item = a_list.pop()
        self.assertEqual(last_item, 3)
        self.assertEqual(a_list, [0, 1, 2, 3])
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the values of `a_list` after `pop` is called
- update the test
    ```python
    def test_removing_the_last_item_of_a_list(self):
        a_list = [0, 1, 2, 3]
        self.assertEqual(a_list, [0, 1, 2, 3])
        last_item = a_list.pop()
        self.assertEqual(last_item, 3)
        self.assertEqual(a_list, [0, 1, 2])
    ```
    the tests pass

## How to get a specific item in a list aka Indexing

to view an item in a list we provide the position as an index in `[]` to the list. `python` uses zero-based indexing which means the position of elements starts at 0
### <span style="color:red">**RED**</span>: make it fail

add a failing test

```python
    def test_getting_items_in_a_list(self):
        a_list = ['first', 'second', 'third', 'fourth']
        self.assertEqual(a_list, ['first', 'second', 'third', 'fourth'])
        self.assertEqual(a_list[0], '')
        self.assertEqual(a_list[2], '')
        self.assertEqual(a_list[1], '')
        self.assertEqual(a_list[3], '')
```

the terminal shows an [AssertionError](./04_ASSERTION_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- update the value on the right for the failing test
    ```python
    def test_getting_items_in_a_list(self):
        a_list = ['first', 'second', 'third', 'fourth']
        self.assertEqual(a_list, ['first', 'second', 'third', 'fourth'])
        self.assertEqual(a_list[0], 'first')
        self.assertEqual(a_list[2], '')
        self.assertEqual(a_list[1], '')
        self.assertEqual(a_list[3], '')
        self.assertEqual(a_list[4], '')
        self.assertEqual(a_list[-1], '')
        self.assertEqual(a_list[-3], '')
        self.assertEqual(a_list[-2], '')
        self.assertEqual(a_list[-4], '')
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the next test
- update the value
    ```python
    def test_getting_items_in_a_list(self):
        a_list = ['first', 'second', 'third', 'fourth']
        self.assertEqual(a_list, ['first', 'second', 'third', 'fourth'])
        self.assertEqual(a_list[0], 'first')
        self.assertEqual(a_list[2], 'third')
        self.assertEqual(a_list[1], '')
        self.assertEqual(a_list[3], '')
        self.assertEqual(a_list[-1], '')
        self.assertEqual(a_list[-3], '')
        self.assertEqual(a_list[-2], '')
        self.assertEqual(a_list[-4], '')
    ```
    the terminal shows a failure for the next test
- update the tests until they all pass

## IndexError

What happens when we try to get an item from a list but use an index that is greater than the number of items in a list

### <span style="color:red">**RED**</span>: make it fail

add a failing test

```python
    def test_indexing_with_a_number_greater_than_the_length_of_the_list(self):
        a_list = ['a', 'b', 'c', 'd']
        self.assertEqual(a_list[5], 'd')
```
the terminal updates to show an [IndexError](https://docs.python.org/3/library/exceptions.html?highlight=exceptions#IndexError)

### <span style="color:green">**GREEN**</span>: make it pass

- add `IndexError` to the running list of exceptions encountered
    ```python
    # Exceptions Encountered
    # AssertionError
    # ModuleNotFoundError
    # AttributeError
    # NameError
    # TypeError
    # SyntaxError
    # IndentationError
    # IndexError
    ```
- add a `self.assertRaises` like we did in [Exception Handling](./05_EXCEPTION_HANDLING.md) to make the test pass
    ```python
    def test_indexing_with_a_number_greater_than_the_length_of_the_list(self):
        a_list = ['a', 'b', 'c', 'd']
        with self.assertRaises(IndexError):
            a_list[5]
    ```
### <span style="color:orange">**REFACTOR**</span>: make it better

## How to view the attributes and methods of a `list`

At the end of [TDD_CLASSES](./08_CLASSES.md) we learned how to view `attributes` and `methods` of an object. Let's do the same for `lists`

### <span style="color:red">**RED**</span>: make it fail

add a failing test

```python
    def test_attributes_and_methods_of_a_list(self):
        self.maxDiff = None
        self.assertEqual(
            dir(list),
            []
        )
```
- `self.maxDiff` is an attribute of the `unittest.TestCase` class that tells python to show every difference between the two values in the `assertEqual` call
- the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

update the test with the expected values

```python
    def test_attributes_and_methods_of_a_list(self):
        self.maxDiff = None
        self.assertEqual(
            dir(list),
            [
                '__add__',
                '__class__',
                '__class_getitem__',
                '__contains__',
                '__delattr__',
                '__delitem__',
                '__dir__',
                '__doc__',
                '__eq__',
                '__format__',
                '__ge__',
                '__getattribute__',
                '__getitem__',
                '__gt__',
                '__hash__',
                '__iadd__',
                '__imul__',
                '__init__',
                '__init_subclass__',
                '__iter__',
                '__le__',
                '__len__',
                '__lt__',
                '__mul__',
                '__ne__',
                '__new__',
                '__reduce__',
                '__reduce_ex__',
                '__repr__',
                '__reversed__',
                '__rmul__',
                '__setattr__',
                '__setitem__',
                '__sizeof__',
                '__str__',
                '__subclasshook__',
                'append',
                'clear',
                'copy',
                'count',
                'extend',
                'index',
                'insert',
                'pop',
                'remove',
                'reverse',
                'sort'
            ]
        )
```

the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

We see more methods listed than what we have reviewed. What do you think each one of them does? We know some already
- append - adds an item to the list
- clear
- copy
- count
- extend
- index
- insert
- pop - removes the last item in the list
- remove - removes the first occurrence of an item in the list
- reverse
- sort

You can add tests for these methods to make sure we see and know what they do. Do you want to [read more about lists](https://docs.python.org/3/tutorial/datastructures.html?highlight=list%20remove#more-on-lists)