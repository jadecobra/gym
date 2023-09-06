# How to solve the AttributeError in python

We will step through solving an `AttributeError` in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Attributes

Attributes are properties/variables/names that belong to an object.
An `AttributeError` is raised when there is a reference an attribute/property/name/variable that does not exist in the object called

## How to solve the AttributeError by defining a Variable

### <span style="color:red">**RED**</span>: make it fail

- Open a new file in the editor and save it as `tests/test_attribute_error.py` in the `tests` folder you created in [Setup Test Driven Development Project](./TDD_SETUP.md) and type the following in the file

    ```python
    import unittest
    import module


    class TestAttributeError(unittest.TestCase):
        def test_defining_variables_to_solve_attribute_errors(self):
            self.assertIsNone(module.variable_0)
    ```
    What is the code above doing?
    - `import unittest` imports the unittest module from the python standard library
    - `import module` import module from somewhere - this is going to hold the solution we write
    - `class TestAttributeError(unittest.TestCase):` - a class definition that inherits from `unittest.TestCase` and will hold our tests
    - `def test_defining_variables_to_solve_attribute_errors(self):` the definition of our first test function. we try to test one thing with our test function. In this case we are testing if definining variables can solve an `AttributeError`
    - `self.assertIsNone(module.variable_0)` - the actual test. This is equivalent to asking the question `is module.variable_0 equal to None`
    - `assertIsNone` is one of the helper functions inherited from `unittest.TestCase`
    - `self` refers to the `TestAttributeError` class

    If you left `pytest-watch` running from [Setup Test Driven Development Project](./TDD_SETUP.md) you should see the following in the terminal
    ```shell
    ImportError while importing test module '/<PATH_TO_PROJECT_NAME>/project_name/tests/test_attribute_error.py'.
    Hint: make sure your test modules/packages have valid python names.
    Traceback:
    /Library/Frameworks/python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py:126: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
    tests/test_attribute_error.py:2: in <module>
        import module
    E   ModuleNotFoundError: No module named 'module'
    ```

    This error was encountered in [00_TDD_MODULE_NOT_FOUND_ERROR](./00_TDD_MODULE_NOT_FOUND_ERROR.md). We know how to solve it.

### <span style="color:green">**GREEN**</span>: make it pass

- create `module.py` in the `project_name` folder and the terminal will update to show the following
    ```shell
    self = <tests.test_attribute_error.TestAttributeError testMethod=test_defining_variables_to_solve_attribute_errors>

        def test_defining_variables_to_solve_attribute_errors(self):
    >       self.assertIsNone(module.variable_0)
    E       AttributeError: module 'module' has no attribute 'variable_0'
    ```
    Looking at the traceback starting from the bottom
    - `tests/test_attribute_error.py:7: AttributeError` the location and name of the Error that causes the failure
    - `E       AttributeError: module 'module' has no attribute 'variable_0'` the module we imported has no definitions named `variable_0`
    - `>       self.assertIsNone(module.variable_0)` the line of code that errored out during execution
    - `def test_defining_variables_to_solve_attribute_errors(self):` the function definition where the error occurs
    - `self = <tests.test_attribute_error.TestAttributeError testMethod=test_defining_variables_to_solve_attribute_errors>` - A reference to the class and method(function) that caused the failure
- Open `module.py` in the Interactive Development Environment(IDE) and add the following
    ```python
    variable_0
    ```
    The terminal will update to show the following
    ```shell
    tests/test_attribute_error.py:2: in <module>
        import module
    module.py:1: in <module>
        variable_0
    E   NameError: name 'variable_0' is not defined
    ```
    - `E   NameError: name 'variable_0' is not defined` this is a new error so we add it to our running list of errors encountered. The running list now looks like this
        ```
        # Exceptions Encountered
        # AssertionError
        # ModuleNotFoundError
        # AttributeError
        # NameError
        ```
        A `NameError` is raised when there is a reference in an object with no definition
        - What is the difference between a `NameError` and an `AttributeError`?
            - An `AttributeError` occurs when there is a reference to a name in an object and the name does not exist e.g. `object.name`
            - A `NameError` occurs when there is a reference to a name with no prior definition
        - What is similar between `ModuleNotFoundError`, `AttributeError` and `NameError`?
    - `variable_0` the offending line
    - `module.py:1: in <module>` the location of the offending line
- Update `module.py` in the Interactive Development Environment(IDE) to
    ```python
    variable_0 = None
    ```
    this explicity defines `variable_0` with a value of `None` and the terminal updates to show a passing test. YES!!!
    ```shell
    collected 2 items

    tests/test_attribute_error.py .                                             [ 50%]
    tests/test_project_name.py .                                                [100%]

    ============================== 2 passed in 0.03s==================================
    ```

> ***What is the difference between `=` and `==` in python?***
> - `=` is used to assign names to objects e.g. `five = 5` means we can later refer to the number `5` with the name `five`
> - `==` is used to check if two things are equal e.g. `5 == 4` means we want to know if `5` is equal to `4`

### <span style="color:orange">**REFACTOR**</span>: make it better

There's not much to do here, we could repeat the above as a drill to make sure we remember the solution

#### <span style="color:red">**RED**</span>: make it fail
- Update `tests/test_attribute_error.py`
    ```python
    import unittest
    import module


    class TestAttributeError(unittest.TestCase):
        def test_defining_variables_to_solve_attribute_errors(self):
            self.assertIsNone(module.variable_0)
            self.assertIsNone(module.variable_1)
    ```
    the terminal will update to show an `AttributeError`
    ```shell
    E       AttributeError: module 'module' has no attribute 'variable_1'
    ```
#### <span style="color:green">**GREEN**</span>: make it pass
- <span style="color:red">**RED**</span>: make it fail - Update `module.py`
    ```python
    variable_0 = None
    variable_1
    ```
    the terminal will update to show a `NameError`
    ```shell
    E   NameError: name 'variable_1' is not defined
    ```
- <span style="color:green">**GREEN**</span>: make it pass - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    ```
    The terminal will update to show passing tests

#### <span style="color:red">**RED**</span>: make it fail
- Update `tests/test_attribute_error.py`
    ```python
    import unittest
    import module


    class TestAttributeError(unittest.TestCase):
        def test_defining_variables_to_solve_attribute_errors(self):
            self.assertIsNone(module.variable_0)
            self.assertIsNone(module.variable_1)
            self.assertIsNone(module.variable_2)
    ```
    the terminal will update to show an `AttributeError`
    ```shell
    >       self.assertIsNone(module.variable_2)
    E       AttributeError: module 'module' has no attribute 'variable_2'
    ```
##### <span style="color:green">**GREEN**</span>: make it pass
- <span style="color:red">**RED**</span>: make it fail - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    variable_2
    ```
    the terminal will update to show a `NameError`
    ```shell
    E   NameError: name 'variable_2' is not defined
    ```
- <span style="color:green">**GREEN**</span>: make it pass - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    variable_2 = None
    ```
    The tests pass

##### <span style="color:red">**RED**</span>: make it fail
- Update `tests/test_attribute_error.py`
    ```python
    import unittest
    import module


    class TestAttributeError(unittest.TestCase):
        def test_defining_variables_to_solve_attribute_errors(self):
            self.assertIsNone(module.variable_0)
            self.assertIsNone(module.variable_1)
            self.assertIsNone(module.variable_2)
            self.assertIsNone(module.variable_3)
    ```
    the terminal will update to show an `AttributeError`
    ```shell
    E       AttributeError: module 'module' has no attribute 'variable_3'
    ```
##### <span style="color:green">**GREEN**</span>: make it pass
- <span style="color:red">**RED**</span>: make it fail - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    variable_2 = None
    variable_3
    ```
    the terminal will update to show a `NameError`
    ```shell
    E   NameError: name 'variable_3' is not defined
    ```
- <span style="color:green">**GREEN**</span>: make it pass - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    variable_2 = None
    variable_3 = None
    ```

***LET'S MAKE A DRILL!!!***
We know the pattern so we can drill it for practice. Update the `TestAttributeError` class in `tests/test_attribute_error.py` by sequentially adding more tests until you get to `self.assertIsNone(module.variable_99)`, you will have 102 statements in total
```python
def test_defining_variables_to_solve_attribute_errors(self):
    self.assertIsNone(module.variable_0)
    self.assertIsNone(module.variable_1)
    self.assertIsNone(module.variable_2)
    self.assertIsNone(module.variable_3)
    ...
    self.assertIsNone(module.variable_99)
    self.assertFalse(module.false)
    self.assertTrue(module.true)
```

Repeat the pattern until all tests pass.
- What's your solution to the last two tests? They are similar to the test for failure in [Setup Test Driven Development Project](./TDD_SETUP.md)
- did you update `module.py` this way?
    ```
    true = True
    false = False
    ```

***WELL DONE!!!***
You now know how to solve
- `AssertionError`
- `ModuleNotFoundError`
- `NameError` using variables
- `AttributeError` using variables

## How to solve the AttributeError by defining a Function
Let us take a look at solving `AttributeError` for functions
### <span style="color:red">**RED**</span>: make it fail

- Update the `TestAttributeError` class in `tests/test_attribute_error.py` with
    ```python
        def test_defining_functions_to_solve_attribute_errors(self):
            self.assertIsNone(module.function_0())
    ```
    the terminal updates to show
    ```shell
    E       AttributeError: module 'module' has no attribute 'function_0'
    ```
    solving it the same way as the previous `AttributeError` we update `module.py`
    ```python
    ...
    function_0 = None
    ```
    the terminal updates to show
    ```shell
    E       TypeError: 'NoneType' object is not callable
    ```
    - we have encountered a new exception `TypeError`
    - a `TypeError` occurs in this case because we `called` an object that was not `callable`
    - What is a callable object? In python, it is any object you can reference that does something other than return a value. You can define a callable as a `class` or a `function`
    - When an object is defined as a callable, we call it by adding parentheses at the end e.g. `function_0()` will call `function_0` in `module.py`
    - Add `TypeError` to our list of exceptions encountered
    ```python
    # Exceptions Encountered
    # AssertionError
    # ModuleNotFoundError
    # AttributeError
    # NameError
    # TypeError
    ```

### <span style="color:green">**GREEN**</span>: make it pass

- change `function_0` in `module.py` to a function by updating `module.py` to
    ```python
    def function_0():
        return None
    ```
    the terminal updates to show tests pass

> ***What is a Function?***
> - A `function` is a named block of code that performs some action or series of actions
> - In python a function always returns something
> - the default return value of a function is `None`
> - the line with `return` is the last executable line of code in a function

### <span style="color:orange">**REFACTOR**</span>: make it better

- Let's make it a drill, update `test_defining_functions_to_solve_attribute_errors` in the `TestAttributeError` class in`tests/test_attribute_error.py` to include
    ```python
    def test_defining_functions_to_solve_attribute_errors(self):
        self.assertIsNone(module.function_0())
        self.assertIsNone(module.function_1())
        self.assertIsNone(module.function_2())
        self.assertIsNone(module.function_3())
        ...
        self.assertIsNone(module.function_99())
    ```
    the terminal updates to show an error
    ```shell
    E       AttributeError: module 'module' has no attribute 'function_1'
    ```
    update `module.py` with the solution until all tests pass

***WELL DONE!!!***
You now know how to solve
- `AssertionError`
- `ModuleNotFoundError`
- `NameError`
- `AttributeError` by defining
    - variables
    - functions

## How to solve the AttributeError by defining a Class

Classes
- A class is a blueprint that represents an object
- It is a collection of functions(methods) and attributes
- Attributes are variables that contain some value
- Methods are functions that perform some action and return a value
- For example if we define a Human class we can have
    - attributes
        - eye color
        - date of birth
    - methods
        - age - return age based on date of birth
        - speak - return words

### <span style="color:red">**RED**</span>: make it fail

- Update the `TestAttributeError` class in `tests/test_attribute_error.py` with
    ```python
        def test_defining_functions_to_solve_attribute_errors(self):
            self.assertIsNone(module.Class0())
    ```
    the terminal updates to show
    ```shell
    E       AttributeError: module 'module' has no attribute 'Class0'
    ```
    Looking at the traceback we see it's the line we added that caused the failure
    - We are familiar with an `AttributeError`
    - This also looks exactly like the tests in `test_defining_functions_to_solve_attribute_errors`
    - What's the difference?

### <span style="color:green">**GREEN**</span>: make it pass
- Update `module.py`
    ```python
    Class0 = None
    ```
    the terminal updates to show a `TypeError`
    ```shell
    E       TypeError: 'NoneType' object is not callable
    ```
    We dealt with a similar issue earlier, let's make `Class0` callable the way we know how. update `module.py`
    ```python
    def Class():
        return None
    ```
    The tests pass! But what is the difference between Classes and Functions? Why are we writing a different set of tests for Classes?

### <span style="color:orange">**REFACTOR**</span>: make it better

- Let's make it a drill. - Update `test_defining_functions_to_solve_attribute_errors` in the `TestAttributeError` class in `tests/test_attribute_error.py`
    ```python
        def test_defining_classes_to_solve_attribute_errors(self):
            self.assertIsNone(module.Class0())
            self.assertIsNone(module.Class1())
            self.assertIsNone(module.Class2())
            self.assertIsNone(module.Class3())
            ...
            self.assertIsNone(module.Class99())
    ```
    the terminal updates to show
    ```shell
        E       AttributeError: module 'module' has no attribute 'Class1'
    ```
    update `module.py` with the solution until all tests pass

***WELL DONE!!!***
You now know how to solve
- `AssertionError`
- `ModuleNotFoundError`
- `NameError`
- `AttributeError` by defining
    - variables
    - functions
    - classes?
        - do we know how to define classes? so far our solution looks the same as defining functions. What's the difference between functions and classes?

## How to solve the AttributeError by defining an Attribute in a Class

### <span style="color:red">**RED**</span>: make it fail

- update the `TestAttributeError` class in `test_attribute_error.py`
    ```python
    def test_defining_attributes_in_classes_to_solve_attribute_errors(self):
        self.assertIsNone(module.Class.attribute_0)
    ```
    the terminal updates to show an `AttributeError`
    ```python
    >       self.assertIsNone(module.Class.attribute_0)
    E       AttributeError: module 'module' has no attribute 'Class'
    ```

### <span style="color:green">**GREEN**</span>: make it pass

- update `module.py`
    ```python
    Class = None
    ```
    the terminal updates to show
    ```shell
    E       AttributeError: 'NoneType' object has no attribute 'attribute_0'
    ```
    update `module.py`
    ```python
    def Class():
        return None
    ```
    the terminal updates to show
    ```shell
    E       AttributeError: 'function' object has no attribute 'attribute_0'
    ```
    how do we define an attribute in a function?
    update `module.py`
    ```python
    def Class():
        attribute_0 = None
        return None
    ```
    the terminal still shows the same error
- update `module.py` to change the definition of `Class` using the `class` keyword instead of `def`
    ```python
    class Class():
        attribute_0 = None
        return None
    ```

    the terminal will update to show a `SyntaxError`
    ```shell
    E       return None
    E       ^^^^^^^^^^^
    E   SyntaxError: 'return' outside function
    ```
    - We have a new error `SyntaxError` add this to the running list of Exceptions
    - The error is caused by the `return` statement being outside of a function
    ```python
    # Exceptions Encountered
    # AssertionError
    # ModuleNotFoundError
    # AttributeError
    # NameError
    # TypeError
    # SyntaxError
    ```
- remove the troublesome line from `module.py`
    ```python
    class Class():
        attribute_0 = None
    ```
    Eureka! The Tests pass!!

### <span style="color:orange">**REFACTOR**</span>: make it better

- The current solution for `test_defining_classes_to_solve_attribute_errors` was done by defining functions but the test says `definining_classes`. Let's update those to use the proper way to define classes. Update `module.py` to use `class` instead of `def` e.g.
    ```python
    class Class0():
        pass
    ```
    `pass` is a keyword used as a placeholder that does nothing
- We now know how to properly define a class and define an attribute. To practice defining an attribute, let's make a drill. Update `test_defining_attributes_in_classes_to_solve_attribute_errors` in `TestAttributeError` in `test_attribute_error.py`
    ```python
    def test_defining_attributes_in_classes_to_solve_attribute_errors(self):
        self.assertIsNone(module.Class.attribute_0)
        self.assertIsNone(module.Class.attribute_1)
        self.assertIsNone(module.Class.attribute_2)
        self.assertIsNone(module.Class.attribute_3)
        ...
        self.assertIsNone(module.Class.attribute_99)
    ```
    the terminal updates to show
    ```shell
    E       AttributeError: type object 'Class' has no attribute 'attribute_1'
    ```
    update `module.py` with the solution until all tests pass

***WELL DONE!!!***
You now know how to solve
- `AssertionError`
- `ModuleNotFoundError`
- `NameError`
- `AttributeError` by defining
    - variables
    - functions
    - classes
    - attributes in classes

## How to solve the AttributeError by defining a Method(Function) in a Class

### <span style="color:red">**RED**</span>: make it fail

- update the `TestAttributeError` class in `test_attribute_error.py`
    ```python
    def test_defining_functions_in_classes_to_solve_attribute_errors(self):
        self.assertIsNone(module.Class.method_0())
    ```
    the terminal updates to show an `AttributeError`
    ```python
    >       self.assertIsNone(module.Class.method_0())
    E       AttributeError: type object 'Class' has no attribute 'method_0'
    ```

### <span style="color:green">**GREEN**</span>: make it pass

- Update the class `Class` in `module.py`
    ```python
    class Class():
        ...
        method_0 = None
    ```
    the terminal will update to show a `TypeError`
    ```shell
    >       self.assertIsNone(module.Class.method_0())
    E       TypeError: 'NoneType' object is not callable
    ```
    this is in our list of errors and we have solved this before
- change `method_0` in the class `Class` in `module.py` to a function to make it callable
    ```python
    class Class():
        ...
        def method_0():
            return None
    ```
    the tests pass. Fantastic

### <span style="color:orange">**REFACTOR**</span>: make it better

You know the `drill`, let's make it. Update `test_defining_functions_in_classes_to_solve_attribute_errors` in `TestAttributeError` in `test_attribute_error.py`
```python
def test_defining_functions_in_classes_to_solve_attribute_errors(self):
    self.assertIsNone(module.Class.method_0())
    self.assertIsNone(module.Class.method_1())
    self.assertIsNone(module.Class.method_2())
    self.assertIsNone(module.Class.method_3())
    ...
    self.assertIsNone(module.Class.method_99())
```
repeat the solution until all tests pass

***WELL DONE!!!***
You now know how to solve
- `AssertionError`
- `ModuleNotFoundError`
- `NameError`
- `AttributeError` by defining
    - variables
    - functions
    - classes
    - attributes in classes
    - functions/methods in classes

***WHAT'S THE DIFFERENCE BETWEEN CLASSES AND FUNCTIONS?***
- we cannot access attributes we define in a function outside the function
- `def` vs `class`
- `snake_case` vs `CamelCase` names
- accessibility of attributes and methods from outside the definitions/declarations