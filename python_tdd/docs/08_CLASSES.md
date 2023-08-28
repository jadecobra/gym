# How to write classes in python

This tutorial will step through clesses in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Classes

`classes` are a template that we can use to represent an object. It is collection of `functions/methods` and `variables/attributes` that belong together

## How to define Class

- use the `class` keyword
- use `TitleCase` for naming
- use Descriptive names

### <span style="color:red">**RED**</span>: make it fail

create a new file named `test_classes.py`
```python
import unittest
import classes


class TestClasses(unittest.TestCase):

    def test_class_definitions_with_pass(self):
        self.assertIsInstance(classes.ClassWithPass(), object)
```
the terminal updates to show a [ModuleNotFoundError](./00_MODULE_NOT_FOUND_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- create a python module named `classes.py` and the terminal updates to show [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add the name `ClassWithPass` to the module
    ```python
    ClassWithPass
    ```
    the terminal updates to show a `NameError`
- update the name to define a variable
    ```python
    ClassWithPass = None
    ```
- redefine the variable as a class
    ```python
    class ClassWithPass:
    ```
    the terminal updates to show an [IndentationError](./02_INDENTATION_ERROR.md)
- add `pass` to the definition like we did in [Functions](./07_FUNCTIONS.md)
    ```python
    class ClassWithPass:
        pass
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

- We learned in [Functions](./07_FUNCTIONS.md) that `pass` is a placeholder.
- In python everything is an `object`, including classes. Our the test `self.assertIsInstance(classes.ClassWithPass(), object)` checks if `ClassWithPass` is an `object`
- What other ways can we define `classes`?

### <span style="color:red">**RED**</span>: make it fail

add another test to `TestClasses` in `test_classes.py`
```python
    def test_classes_definitions_with_parentheses(self):
        self.assertIsInstance(classes.ClassWithParentheses(), object)
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- update `classes.py` with a class definition
    ```python
    class ClassWithParentheses:
        pass
    ```
    the terminal updates to show passing tests
- update the definition to include parentheses
    ```python
    class ClassWithParentheses():
        pass
    ```
    the terminal shows all tests are still passing.
- We now know that we can define `classes`
    - with parentheses
    - without parentheses
    - `pass` is a placeholder

### <span style="color:orange">**REFACTOR**</span>: make it better

In object oriented programming there is a concept called [Inheritance]() and just like genetic inheritance in biology we can define `objects` that inherit from other `objects`.

To do this we specify the parent in parentheses when we define the child, to establish the relationship

### <span style="color:red">**RED**</span>: make it fail

add another test to `TestClasses` in `test_classes.py`
```python
    def test_class_definition_with_object(self):
        self.assertIsInstance(classes.ClassWithObject(), object)
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a class definition to `classes.py`
    ```python
    class ClassWithObject():
        pass
    ```
    the terminal updates to show passing tests
- update the definition to explicitly state the parent `object`
    ```python
    class ClassWithObject(object):
        pass
    ```
    the terminal updates to show passing tests

We now know that in python
- classes can be defined
    - with parentheses explicitly stating what object the class inherits from
    - without parentheses
    - pass is a placeholder
- classes inherit from the `object` class, because in each of our tests, whether explicitly stated or not, the class is an `instance` of an `object`
- what is an [object](https://docs.python.org/3/glossary.html#term-object)?

***RULE OF THUMB***
> From [the zen of python](https://peps.python.org/pep-0020/)
> `Explicit is better than implicit.`
> We will use the explicit form of class definitions with the parent `object` in parentheses


### <span style="color:orange">**REFACTOR**</span>: make it better

## Class Attributes

Since we know how to define a class, let's add some tests for attributes. update `TestClasses` in `classes.py`
```python
    def test_classes_with_attributes(self):
        self.assertEqual(classes.ClassWithAttributes.an_integer, int)
```
the terminal updates to show [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:red">**RED**</span>: make it fail

update `classes.py` with a `class` definition
```python
class ClassWithAttributes(object):
    pass
```
the terminal updates to show another [AttributeError](./01_ATTRIBUTE_ERROR.md), this time for a missing attribute in our newly defined class

### <span style="color:green">**GREEN**</span>: make it pass

- add an attribute to `ClassWithAttributes`
    ```python
    class ClassWithAttributes(object):
        a_boolean
    ```
    the terminal updates to show a `NameError`
- update the name with a definition
    ```python
    class ClassWithAttributes(object):
        a_boolean = None
    ```
    the terminal updates show an [AssertionError](./04_ASSERTION_ERROR.md)
- redefine the attribute to make the test pass
    ```python
    class ClassWithAttributes(object):
        a_boolean = bool
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's repeat this with other python `objects/data structures`

### <span style="color:red">**RED**</span>: make it fail

update `test_classes_with_attributes` with more tests
```python
    def test_classes_with_attributes(self):
        self.assertEqual(classes.ClassWithAttributes.a_boolean, bool)
        self.assertEqual(classes.ClassWithAttributes.an_integer, int)
        self.assertEqual(classes.ClassWithAttributes.a_float, float)
        self.assertEqual(classes.ClassWithAttributes.a_string, str)
        self.assertEqual(classes.ClassWithAttributes.a_tuple, tuple)
        self.assertEqual(classes.ClassWithAttributes.a_list, list)
        self.assertEqual(classes.ClassWithAttributes.a_set, set)
        self.assertEqual(classes.ClassWithAttributes.a_dictionary, dict)
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

update `ClassWithAttributes` with attributes sto make the tests pass
```python
class ClassWithAttributes(object):
    a_boolean = bool
    an_integer = int
    a_float = float
    a_string = str
    a_tuple = tuple
    a_list = list
    a_set = set
    a_dictionary = dict
```
the terminal updates to show passing tests

## Class Methods

### <span style="color:red">**RED**</span>: make it fail
### <span style="color:green">**GREEN**</span>: make it pass
### <span style="color:orange">**REFACTOR**</span>: make it better