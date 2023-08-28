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

Since we know how to define a class, let's add some tests for attributes.

### <span style="color:red">**RED**</span>: make it fail
- update `TestClasses` in `classes.py`
    ```python
        def test_classes_with_attributes(self):
            self.assertEqual(classes.ClassWithAttributes.an_integer, int)
    ```
    the terminal updates to show [AttributeError](./01_ATTRIBUTE_ERROR.md)
- update `classes.py` with a `class` definition
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

Classes can have `methods/functions`

### <span style="color:red">**RED**</span>: make it fail

Let us add some tests for class methods. update `TestClasses` in `classes.py`
```python
    def test_classes_with_methods(self):
        self.assertEqual(classes.ClassWithMethods.method_a(), 'You called MethodA')
```
the terminal updates to show [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- update `classes.py` with a class definition
    ```python


    class ClassWithMethods(object):

        pass
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add an attribute to the `ClassWithMethods`
    ```python


    class ClassWithMethods(object):

        method_a
    ```
    the terminal updates to show a `Nameerror`
- define `method_a` as an attribute
    ```python


    class ClassWithMethods(object):

        method_a = None
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md) since `method_a` is not callable
- update the definition of `method_a` to make it a function
    ```python


    class ClassWithMethods(object):

        def method_a():
            return None
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
-  change the value the function returns to match the expectation in our test
    ```python
        def method_a():
            return 'You called MethodA'
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

- Let's add a few more tests for fun to `test_classes_with_methods`
    ```python
        def test_classes_with_methods(self):
            self.assertEqual(classes.ClassWithMethods.method_a(), 'You called MethodA')
            self.assertEqual(classes.ClassWithMethods.method_b(), 'You called MethodB')
            self.assertEqual(classes.ClassWithMethods.method_c(), 'You called MethodC')
            self.assertEqual(classes.ClassWithMethods.method_d(), 'You called MethodD')
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- update `ClassWithmethods` to make it pass
- let's add another test for a class that has both attributes and methods
    ```python
        def test_classes_with_attributes_and_methods(self):
            self.assertEqual(classes.ClassWithAttributesAndMethods.attribute, 'attribute')
            self.assertEqual(classes.ClassWithAttributesAndMethods.method(), 'you called a method')
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- update `classes.py` to make the tests pass by defining the class, attribute and methods
    ```python


    class ClassWithAttributesAndMethods(object):

        attribute = 'attribute'

        def method():
            return 'you called a method'
    ```
    the terminal updates to show passing tests


## Class Initializers

CONGRATULATIONS. You now know how to define classes, attributes and methods. Let's expand on this knowledge. How do we use classes?

### <span style="color:red">**RED**</span>: make it fail

add a test to `test_clases.py`
```python
    def test_classes_with_initializers(self):
        self.assertEqual(classes.Boy().sex, 'M')
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- add a definition for the class
    ```python


    class Boy(object):

        pass
    ```
    the terminal updates to show another [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add the name `sex` to the `Boy` class
    ```oython


    class Boy(object):

        sex
    ```
    the terminal updates to show a `NameError`
- add a definition for the `sex` attribute
    ```python


    class Boy(object):

        sex = 'M
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

- Let's add another test to `test_classes_with_initializers`
    ```python
            self.assertEqual(classes.Girl(sex='F').sex, 'F')
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- update `classes.py` with a definition for the `Girl` class
    ```python


    class Girl(object):

        sex = 'M'
    ```
    the terminal updates to show
    ```python
    TypeError: Girl() takes no arguments
    ```
    here we see a similarity between `classes` and [functions](./07_FUNCTIONS.md)
    - the call `classes.Girl(sex='F')` looks like a call to a function with keyword arguments
    - How do we define classes to accept keyword arguments when the definition of a class defines the parent it inherits from e.g. `class Class(object)`? We use an initializer
    - What's an initializer? a class method that allows customization of `instances/copies` of a `class`
- add an initiializer to the `Girl` class
    ```python


    class Girl(object):

        sex = 'F'

        def __init__(self):
            pass
    ```
    the terminal updates to show
    ```python
    TypeError: __init__() got an unexpected keyword argument 'sex'
    ```
- update the signature of the `__init__` method to accept a keyword argument
    ```python
    def __init__(self, sex=None):
        pass
    ```
    the terminal updates to show passing tests
- let's add another test we can use an initializer with to `test_classes_with_initializers`
    ```python
        self.assertEqual(classes.Other(sex='?').sex, '?')
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add a class definition to `classes.py`
    ```python


    class Other(object):

    sex = '?'

    def __init__(self, sex=None):
        pass
    ```
    the terminal updates to show passing tests
- Wait a minute, we just repeated the same thing twice.
    - We defined a `class` with a name
    - defined an attribute named `sex`
    - defined an `__init__` method which takes in a `sex` keyword argument
- let's make the repetition complete by redefining the `Boy` class to match the `Girl` and `Other` class
    ```python


    class Boy(object):

        sex = 'M'

        def __init__(self, sex=None):
            pass
    ```
    the terminal shows tests are still passing. Now we have written the same thing 3 times, how can we remove this duplication? Inheritance/Abstraction
- We have 3 classes that are defined in exactly the same way, how can we abstract these things to a parent class that they inherit from? add a new class called `Human` to `classes.py` before the definition for `Boy`
    ```python


    class Human(object):

        sex = 'M'

        def __init__(self, sex='M'):
            pass


    class Boy(object):
        ...
    ```
    the terminal still shows passing tests
- Update the definitions for `Boy` to inherit from the `Human` class
    ```python
    class Boy(Human):
        ...
    ```
    the terminal shows passing tests
- remove the `sex` attribute from the `Boy` class and the tests continue to pass
- remove the `__init__` method, updating the class definition
    ```python


    class Boy(Human):

        pass
    ```
    the terminal still shows passing tests
- Let's try the same thing with the `Girl` class. update the definition to inherit from the `Human` class
    ```python
    class Girl(Human):
        ...
    ```
    the terminal shows passing tests
- remove the `sex` attribute and the terminal shows an [AssertionError](./04_ASSERTION_ERROR.md)
- update the `Human` class to set the `sex` attribute in the initializer instead of at the class level
    ```python
    class Human(object):

        sex = 'M'

        def __init__(self, sex='M'):
            self.sex = sex
    ```
    the terminal still shows an [AssertionError](./04_ASSERTION_ERROR.md)
- remove the `__init__` method from the `Girl` class
    ```python
    class Girl(Human):

        pass
    ```
    the terminal updates to show passing tests
- can we do the same with the `Other` class? update the definition of the class to inherit from the `Human` class
    ```python
    class Other(Human):

        pass
    ```
    the terminal updates to show passing tests.
- one last change, we remove the `sex` attribute from the `Human` class
    ```python
    class Human(object):

        def __init__(self, sex='M'):
            self.sex = sex
    ```
    the terminal still shows passing tests

Why did that work?
- the `Boy`, `Girl` and `Other` class now inherit from the `Human` class which means they all get the same methods and attributes that the `Human` class has, including the `__init__` method
- `self.sex` within each class refers to the `sex` attribute in the class, allowing its definition from the `__init__` method

***CONGRATULATIONS***
- YOu know 