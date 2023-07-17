# How to solve the AttributeError in Python

This tutorial will step through solving an `AttributeError`` in Python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Attributes

Attributes are properties/variables/names that belong to an object.
An `AttributeError` is raised when there is a reference an attribute/property/name/variable that does not exist in the object called

## How to solve the AttributeError by defining a Variable

### <span style="color:red">**RED**</span>: Write a failing test

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
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    /Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py:126: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
    tests/test_attribute_error.py:2: in <module>
        import module
    E   ModuleNotFoundError: No module named 'module'
    ```

    This error was encountered in [00_TDD_MODULE_NOT_FOUND_ERROR](./00_TDD_MODULE_NOT_FOUND_ERROR.md). We know how to solve it.

### <span style="color:green">**GREEN**</span>: Make it Pass

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

### <span style="color:orange">**REFACTOR**</span> - make it better

There's not much to do here, we could repeat the above as a drill to make sure we remember the solution

#### <span style="color:red">**RED**</span>: Write a failing test
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
#### <span style="color:green">**GREEN**</span>: Make it Pass
- <span style="color:red">**RED**</span>: Write a failing test - Update `module.py`
    ```python
    variable_0 = None
    variable_1
    ```
    the terminal will update to show a `NameError`
    ```shell
    E   NameError: name 'variable_1' is not defined
    ```
- <span style="color:green">**GREEN**</span>: Make it Pass - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    ```
    The terminal will update to show passing tests

#### <span style="color:red">**RED**</span>: Write a failing test
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
##### <span style="color:green">**GREEN**</span>: Make it Pass
- <span style="color:red">**RED**</span>: Write a failing test - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    variable_2
    ```
    the terminal will update to show a `NameError`
    ```shell
    E   NameError: name 'variable_2' is not defined
    ```
- <span style="color:green">**GREEN**</span>: Make it Pass - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    variable_2 = None
    ```
    The tests pass

##### <span style="color:red">**RED**</span>: Write a failing test
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
##### <span style="color:green">**GREEN**</span>: Make it Pass
- <span style="color:red">**RED**</span>: Write a failing test - Update `module.py`
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
- <span style="color:green">**GREEN**</span>: Make it Pass - Update `module.py`
    ```python
    variable_0 = None
    variable_1 = None
    variable_2 = None
    variable_3 = None
    ```

This is the pattern. Update the `TestAttributeError` class in `tests/test_attribute_error.py` to add more tests
```python
def test_defining_variables_to_solve_attribute_errors(self):
    self.assertIsNone(module.variable_0)
    self.assertIsNone(module.variable_1)
    self.assertIsNone(module.variable_2)
    self.assertIsNone(module.variable_3)
    self.assertIsNone(module.variable_4)
    self.assertIsNone(module.variable_5)
    self.assertIsNone(module.variable_6)
    self.assertIsNone(module.variable_7)
    self.assertIsNone(module.variable_8)
    self.assertIsNone(module.variable_9)
    self.assertIsNone(module.variable_10)
    self.assertIsNone(module.variable_11)
    self.assertIsNone(module.variable_12)
    self.assertIsNone(module.variable_13)
    self.assertIsNone(module.variable_14)
    self.assertIsNone(module.variable_15)
    self.assertIsNone(module.variable_16)
    self.assertIsNone(module.variable_17)
    self.assertIsNone(module.variable_18)
    self.assertIsNone(module.variable_19)
    self.assertIsNone(module.variable_20)
    self.assertIsNone(module.variable_21)
    self.assertIsNone(module.variable_22)
    self.assertIsNone(module.variable_23)
    self.assertIsNone(module.variable_24)
    self.assertIsNone(module.variable_25)
    self.assertIsNone(module.variable_26)
    self.assertIsNone(module.variable_27)
    self.assertIsNone(module.variable_28)
    self.assertIsNone(module.variable_29)
    self.assertIsNone(module.variable_30)
    self.assertIsNone(module.variable_34)
    self.assertIsNone(module.variable_32)
    self.assertIsNone(module.variable_33)
    self.assertIsNone(module.variable_34)
    self.assertIsNone(module.variable_35)
    self.assertIsNone(module.variable_36)
    self.assertIsNone(module.variable_37)
    self.assertIsNone(module.variable_38)
    self.assertIsNone(module.variable_39)
    self.assertIsNone(module.variable_40)
    self.assertIsNone(module.variable_41)
    self.assertIsNone(module.variable_42)
    self.assertIsNone(module.variable_43)
    self.assertIsNone(module.variable_44)
    self.assertIsNone(module.variable_45)
    self.assertIsNone(module.variable_46)
    self.assertIsNone(module.variable_47)
    self.assertIsNone(module.variable_48)
    self.assertIsNone(module.variable_49)
    self.assertIsNone(module.variable_50)
    self.assertIsNone(module.variable_51)
    self.assertIsNone(module.variable_52)
    self.assertIsNone(module.variable_53)
    self.assertIsNone(module.variable_54)
    self.assertIsNone(module.variable_55)
    self.assertIsNone(module.variable_56)
    self.assertIsNone(module.variable_57)
    self.assertIsNone(module.variable_58)
    self.assertIsNone(module.variable_59)
    self.assertIsNone(module.variable_60)
    self.assertIsNone(module.variable_61)
    self.assertIsNone(module.variable_62)
    self.assertIsNone(module.variable_63)
    self.assertIsNone(module.variable_64)
    self.assertIsNone(module.variable_65)
    self.assertIsNone(module.variable_66)
    self.assertIsNone(module.variable_67)
    self.assertIsNone(module.variable_68)
    self.assertIsNone(module.variable_69)
    self.assertIsNone(module.variable_70)
    self.assertIsNone(module.variable_71)
    self.assertIsNone(module.variable_72)
    self.assertIsNone(module.variable_73)
    self.assertIsNone(module.variable_74)
    self.assertIsNone(module.variable_75)
    self.assertIsNone(module.variable_76)
    self.assertIsNone(module.variable_77)
    self.assertIsNone(module.variable_78)
    self.assertIsNone(module.variable_79)
    self.assertIsNone(module.variable_80)
    self.assertIsNone(module.variable_81)
    self.assertIsNone(module.variable_82)
    self.assertIsNone(module.variable_83)
    self.assertIsNone(module.variable_84)
    self.assertIsNone(module.variable_85)
    self.assertIsNone(module.variable_86)
    self.assertIsNone(module.variable_87)
    self.assertIsNone(module.variable_88)
    self.assertIsNone(module.variable_89)
    self.assertIsNone(module.variable_90)
    self.assertIsNone(module.variable_91)
    self.assertIsNone(module.variable_92)
    self.assertIsNone(module.variable_93)
    self.assertIsNone(module.variable_94)
    self.assertIsNone(module.variable_95)
    self.assertIsNone(module.variable_96)
    self.assertIsNone(module.variable_97)
    self.assertIsNone(module.variable_98)
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
### <span style="color:red">**RED**</span>: Write a failing test

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

### <span style="color:green">**GREEN**</span>: Make it Pass

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

### <span style="color:orange">**REFACTOR**</span> - make it better

- Let's make it a drill, update `test_defining_functions_to_solve_attribute_errors` in the `TestAttributeError` class in`tests/test_attribute_error.py` to include
    ```python
    def test_defining_functions_to_solve_attribute_errors(self):
        self.assertIsNone(module.function_0())
        self.assertIsNone(module.function_1())
        self.assertIsNone(module.function_2())
        self.assertIsNone(module.function_3())
        self.assertIsNone(module.function_4())
        self.assertIsNone(module.function_5())
        self.assertIsNone(module.function_6())
        self.assertIsNone(module.function_7())
        self.assertIsNone(module.function_8())
        self.assertIsNone(module.function_9())
        self.assertIsNone(module.function_10())
        self.assertIsNone(module.function_11())
        self.assertIsNone(module.function_12())
        self.assertIsNone(module.function_13())
        self.assertIsNone(module.function_14())
        self.assertIsNone(module.function_15())
        self.assertIsNone(module.function_16())
        self.assertIsNone(module.function_17())
        self.assertIsNone(module.function_18())
        self.assertIsNone(module.function_19())
        self.assertIsNone(module.function_20())
        self.assertIsNone(module.function_21())
        self.assertIsNone(module.function_22())
        self.assertIsNone(module.function_23())
        self.assertIsNone(module.function_24())
        self.assertIsNone(module.function_25())
        self.assertIsNone(module.function_26())
        self.assertIsNone(module.function_27())
        self.assertIsNone(module.function_28())
        self.assertIsNone(module.function_29())
        self.assertIsNone(module.function_30())
        self.assertIsNone(module.function_34())
        self.assertIsNone(module.function_32())
        self.assertIsNone(module.function_33())
        self.assertIsNone(module.function_34())
        self.assertIsNone(module.function_35())
        self.assertIsNone(module.function_36())
        self.assertIsNone(module.function_37())
        self.assertIsNone(module.function_38())
        self.assertIsNone(module.function_39())
        self.assertIsNone(module.function_40())
        self.assertIsNone(module.function_41())
        self.assertIsNone(module.function_42())
        self.assertIsNone(module.function_43())
        self.assertIsNone(module.function_44())
        self.assertIsNone(module.function_45())
        self.assertIsNone(module.function_46())
        self.assertIsNone(module.function_47())
        self.assertIsNone(module.function_48())
        self.assertIsNone(module.function_49())
        self.assertIsNone(module.function_50())
        self.assertIsNone(module.function_51())
        self.assertIsNone(module.function_52())
        self.assertIsNone(module.function_53())
        self.assertIsNone(module.function_54())
        self.assertIsNone(module.function_55())
        self.assertIsNone(module.function_56())
        self.assertIsNone(module.function_57())
        self.assertIsNone(module.function_58())
        self.assertIsNone(module.function_59())
        self.assertIsNone(module.function_60())
        self.assertIsNone(module.function_61())
        self.assertIsNone(module.function_62())
        self.assertIsNone(module.function_63())
        self.assertIsNone(module.function_64())
        self.assertIsNone(module.function_65())
        self.assertIsNone(module.function_66())
        self.assertIsNone(module.function_67())
        self.assertIsNone(module.function_68())
        self.assertIsNone(module.function_69())
        self.assertIsNone(module.function_70())
        self.assertIsNone(module.function_71())
        self.assertIsNone(module.function_72())
        self.assertIsNone(module.function_73())
        self.assertIsNone(module.function_74())
        self.assertIsNone(module.function_75())
        self.assertIsNone(module.function_76())
        self.assertIsNone(module.function_77())
        self.assertIsNone(module.function_78())
        self.assertIsNone(module.function_79())
        self.assertIsNone(module.function_80())
        self.assertIsNone(module.function_81())
        self.assertIsNone(module.function_82())
        self.assertIsNone(module.function_83())
        self.assertIsNone(module.function_84())
        self.assertIsNone(module.function_85())
        self.assertIsNone(module.function_86())
        self.assertIsNone(module.function_87())
        self.assertIsNone(module.function_88())
        self.assertIsNone(module.function_89())
        self.assertIsNone(module.function_90())
        self.assertIsNone(module.function_91())
        self.assertIsNone(module.function_92())
        self.assertIsNone(module.function_93())
        self.assertIsNone(module.function_94())
        self.assertIsNone(module.function_95())
        self.assertIsNone(module.function_96())
        self.assertIsNone(module.function_97())
        self.assertIsNone(module.function_98())
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

### <span style="color:red">**RED**</span>: Write a failing test

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

### <span style="color:green">**GREEN**</span>: Make it Pass
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

### <span style="color:orange">**REFACTOR**</span> - make it better

- Let's make it a drill. - Update `test_defining_functions_to_solve_attribute_errors` in the `TestAttributeError` class in `tests/test_attribute_error.py`
    ```python
        def test_defining_classes_to_solve_attribute_errors(self):
            self.assertIsNone(module.Class0())
            self.assertIsNone(module.Class1())
            self.assertIsNone(module.Class2())
            self.assertIsNone(module.Class3())
            self.assertIsNone(module.Class4())
            self.assertIsNone(module.Class5())
            self.assertIsNone(module.Class6())
            self.assertIsNone(module.Class7())
            self.assertIsNone(module.Class8())
            self.assertIsNone(module.Class9())
            self.assertIsNone(module.Class10())
            self.assertIsNone(module.Class11())
            self.assertIsNone(module.Class12())
            self.assertIsNone(module.Class13())
            self.assertIsNone(module.Class14())
            self.assertIsNone(module.Class15())
            self.assertIsNone(module.Class16())
            self.assertIsNone(module.Class17())
            self.assertIsNone(module.Class18())
            self.assertIsNone(module.Class19())
            self.assertIsNone(module.Class20())
            self.assertIsNone(module.Class21())
            self.assertIsNone(module.Class22())
            self.assertIsNone(module.Class23())
            self.assertIsNone(module.Class24())
            self.assertIsNone(module.Class25())
            self.assertIsNone(module.Class26())
            self.assertIsNone(module.Class27())
            self.assertIsNone(module.Class28())
            self.assertIsNone(module.Class29())
            self.assertIsNone(module.Class30())
            self.assertIsNone(module.Class34())
            self.assertIsNone(module.Class32())
            self.assertIsNone(module.Class33())
            self.assertIsNone(module.Class34())
            self.assertIsNone(module.Class35())
            self.assertIsNone(module.Class36())
            self.assertIsNone(module.Class37())
            self.assertIsNone(module.Class38())
            self.assertIsNone(module.Class39())
            self.assertIsNone(module.Class40())
            self.assertIsNone(module.Class41())
            self.assertIsNone(module.Class42())
            self.assertIsNone(module.Class43())
            self.assertIsNone(module.Class44())
            self.assertIsNone(module.Class45())
            self.assertIsNone(module.Class46())
            self.assertIsNone(module.Class47())
            self.assertIsNone(module.Class48())
            self.assertIsNone(module.Class49())
            self.assertIsNone(module.Class50())
            self.assertIsNone(module.Class51())
            self.assertIsNone(module.Class52())
            self.assertIsNone(module.Class53())
            self.assertIsNone(module.Class54())
            self.assertIsNone(module.Class55())
            self.assertIsNone(module.Class56())
            self.assertIsNone(module.Class57())
            self.assertIsNone(module.Class58())
            self.assertIsNone(module.Class59())
            self.assertIsNone(module.Class60())
            self.assertIsNone(module.Class61())
            self.assertIsNone(module.Class62())
            self.assertIsNone(module.Class63())
            self.assertIsNone(module.Class64())
            self.assertIsNone(module.Class65())
            self.assertIsNone(module.Class66())
            self.assertIsNone(module.Class67())
            self.assertIsNone(module.Class68())
            self.assertIsNone(module.Class69())
            self.assertIsNone(module.Class70())
            self.assertIsNone(module.Class71())
            self.assertIsNone(module.Class72())
            self.assertIsNone(module.Class73())
            self.assertIsNone(module.Class74())
            self.assertIsNone(module.Class75())
            self.assertIsNone(module.Class76())
            self.assertIsNone(module.Class77())
            self.assertIsNone(module.Class78())
            self.assertIsNone(module.Class79())
            self.assertIsNone(module.Class80())
            self.assertIsNone(module.Class81())
            self.assertIsNone(module.Class82())
            self.assertIsNone(module.Class83())
            self.assertIsNone(module.Class84())
            self.assertIsNone(module.Class85())
            self.assertIsNone(module.Class86())
            self.assertIsNone(module.Class87())
            self.assertIsNone(module.Class88())
            self.assertIsNone(module.Class89())
            self.assertIsNone(module.Class90())
            self.assertIsNone(module.Class91())
            self.assertIsNone(module.Class92())
            self.assertIsNone(module.Class93())
            self.assertIsNone(module.Class94())
            self.assertIsNone(module.Class95())
            self.assertIsNone(module.Class96())
            self.assertIsNone(module.Class97())
            self.assertIsNone(module.Class98())
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

### <span style="color:red">**RED**</span>: Write a failing test

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

### <span style="color:green">**GREEN**</span>: Make it Pass

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

### <span style="color:orange">**REFACTOR**</span> - make it better

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
        self.assertIsNone(module.Class.attribute_4)
        self.assertIsNone(module.Class.attribute_5)
        self.assertIsNone(module.Class.attribute_6)
        self.assertIsNone(module.Class.attribute_7)
        self.assertIsNone(module.Class.attribute_8)
        self.assertIsNone(module.Class.attribute_9)
        self.assertIsNone(module.Class.attribute_10)
        self.assertIsNone(module.Class.attribute_11)
        self.assertIsNone(module.Class.attribute_12)
        self.assertIsNone(module.Class.attribute_13)
        self.assertIsNone(module.Class.attribute_14)
        self.assertIsNone(module.Class.attribute_15)
        self.assertIsNone(module.Class.attribute_16)
        self.assertIsNone(module.Class.attribute_17)
        self.assertIsNone(module.Class.attribute_18)
        self.assertIsNone(module.Class.attribute_19)
        self.assertIsNone(module.Class.attribute_20)
        self.assertIsNone(module.Class.attribute_21)
        self.assertIsNone(module.Class.attribute_22)
        self.assertIsNone(module.Class.attribute_23)
        self.assertIsNone(module.Class.attribute_24)
        self.assertIsNone(module.Class.attribute_25)
        self.assertIsNone(module.Class.attribute_26)
        self.assertIsNone(module.Class.attribute_27)
        self.assertIsNone(module.Class.attribute_28)
        self.assertIsNone(module.Class.attribute_29)
        self.assertIsNone(module.Class.attribute_30)
        self.assertIsNone(module.Class.attribute_34)
        self.assertIsNone(module.Class.attribute_32)
        self.assertIsNone(module.Class.attribute_33)
        self.assertIsNone(module.Class.attribute_34)
        self.assertIsNone(module.Class.attribute_35)
        self.assertIsNone(module.Class.attribute_36)
        self.assertIsNone(module.Class.attribute_37)
        self.assertIsNone(module.Class.attribute_38)
        self.assertIsNone(module.Class.attribute_39)
        self.assertIsNone(module.Class.attribute_40)
        self.assertIsNone(module.Class.attribute_41)
        self.assertIsNone(module.Class.attribute_42)
        self.assertIsNone(module.Class.attribute_43)
        self.assertIsNone(module.Class.attribute_44)
        self.assertIsNone(module.Class.attribute_45)
        self.assertIsNone(module.Class.attribute_46)
        self.assertIsNone(module.Class.attribute_47)
        self.assertIsNone(module.Class.attribute_48)
        self.assertIsNone(module.Class.attribute_49)
        self.assertIsNone(module.Class.attribute_50)
        self.assertIsNone(module.Class.attribute_51)
        self.assertIsNone(module.Class.attribute_52)
        self.assertIsNone(module.Class.attribute_53)
        self.assertIsNone(module.Class.attribute_54)
        self.assertIsNone(module.Class.attribute_55)
        self.assertIsNone(module.Class.attribute_56)
        self.assertIsNone(module.Class.attribute_57)
        self.assertIsNone(module.Class.attribute_58)
        self.assertIsNone(module.Class.attribute_59)
        self.assertIsNone(module.Class.attribute_60)
        self.assertIsNone(module.Class.attribute_61)
        self.assertIsNone(module.Class.attribute_62)
        self.assertIsNone(module.Class.attribute_63)
        self.assertIsNone(module.Class.attribute_64)
        self.assertIsNone(module.Class.attribute_65)
        self.assertIsNone(module.Class.attribute_66)
        self.assertIsNone(module.Class.attribute_67)
        self.assertIsNone(module.Class.attribute_68)
        self.assertIsNone(module.Class.attribute_69)
        self.assertIsNone(module.Class.attribute_70)
        self.assertIsNone(module.Class.attribute_71)
        self.assertIsNone(module.Class.attribute_72)
        self.assertIsNone(module.Class.attribute_73)
        self.assertIsNone(module.Class.attribute_74)
        self.assertIsNone(module.Class.attribute_75)
        self.assertIsNone(module.Class.attribute_76)
        self.assertIsNone(module.Class.attribute_77)
        self.assertIsNone(module.Class.attribute_78)
        self.assertIsNone(module.Class.attribute_79)
        self.assertIsNone(module.Class.attribute_80)
        self.assertIsNone(module.Class.attribute_81)
        self.assertIsNone(module.Class.attribute_82)
        self.assertIsNone(module.Class.attribute_83)
        self.assertIsNone(module.Class.attribute_84)
        self.assertIsNone(module.Class.attribute_85)
        self.assertIsNone(module.Class.attribute_86)
        self.assertIsNone(module.Class.attribute_87)
        self.assertIsNone(module.Class.attribute_88)
        self.assertIsNone(module.Class.attribute_89)
        self.assertIsNone(module.Class.attribute_90)
        self.assertIsNone(module.Class.attribute_91)
        self.assertIsNone(module.Class.attribute_92)
        self.assertIsNone(module.Class.attribute_93)
        self.assertIsNone(module.Class.attribute_94)
        self.assertIsNone(module.Class.attribute_95)
        self.assertIsNone(module.Class.attribute_96)
        self.assertIsNone(module.Class.attribute_97)
        self.assertIsNone(module.Class.attribute_98)
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

### <span style="color:red">**RED**</span>: Write a failing test

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

### <span style="color:green">**GREEN**</span>: Make it Pass

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

### <span style="color:orange">**REFACTOR**</span> - make it better

You know the `drill`, let's make it. Update `test_defining_functions_in_classes_to_solve_attribute_errors` in `TestAttributeError` in `test_attribute_error.py`
```python
def test_defining_functions_in_classes_to_solve_attribute_errors(self):
    self.assertIsNone(module.Class.method_0())
    self.assertIsNone(module.Class.method_1())
    self.assertIsNone(module.Class.method_2())
    self.assertIsNone(module.Class.method_3())
    self.assertIsNone(module.Class.method_4())
    self.assertIsNone(module.Class.method_5())
    self.assertIsNone(module.Class.method_6())
    self.assertIsNone(module.Class.method_7())
    self.assertIsNone(module.Class.method_8())
    self.assertIsNone(module.Class.method_9())
    self.assertIsNone(module.Class.method_10())
    self.assertIsNone(module.Class.method_11())
    self.assertIsNone(module.Class.method_12())
    self.assertIsNone(module.Class.method_13())
    self.assertIsNone(module.Class.method_14())
    self.assertIsNone(module.Class.method_15())
    self.assertIsNone(module.Class.method_16())
    self.assertIsNone(module.Class.method_17())
    self.assertIsNone(module.Class.method_18())
    self.assertIsNone(module.Class.method_19())
    self.assertIsNone(module.Class.method_20())
    self.assertIsNone(module.Class.method_21())
    self.assertIsNone(module.Class.method_22())
    self.assertIsNone(module.Class.method_23())
    self.assertIsNone(module.Class.method_24())
    self.assertIsNone(module.Class.method_25())
    self.assertIsNone(module.Class.method_26())
    self.assertIsNone(module.Class.method_27())
    self.assertIsNone(module.Class.method_28())
    self.assertIsNone(module.Class.method_29())
    self.assertIsNone(module.Class.method_30())
    self.assertIsNone(module.Class.method_34())
    self.assertIsNone(module.Class.method_32())
    self.assertIsNone(module.Class.method_33())
    self.assertIsNone(module.Class.method_34())
    self.assertIsNone(module.Class.method_35())
    self.assertIsNone(module.Class.method_36())
    self.assertIsNone(module.Class.method_37())
    self.assertIsNone(module.Class.method_38())
    self.assertIsNone(module.Class.method_39())
    self.assertIsNone(module.Class.method_40())
    self.assertIsNone(module.Class.method_41())
    self.assertIsNone(module.Class.method_42())
    self.assertIsNone(module.Class.method_43())
    self.assertIsNone(module.Class.method_44())
    self.assertIsNone(module.Class.method_45())
    self.assertIsNone(module.Class.method_46())
    self.assertIsNone(module.Class.method_47())
    self.assertIsNone(module.Class.method_48())
    self.assertIsNone(module.Class.method_49())
    self.assertIsNone(module.Class.method_50())
    self.assertIsNone(module.Class.method_51())
    self.assertIsNone(module.Class.method_52())
    self.assertIsNone(module.Class.method_53())
    self.assertIsNone(module.Class.method_54())
    self.assertIsNone(module.Class.method_55())
    self.assertIsNone(module.Class.method_56())
    self.assertIsNone(module.Class.method_57())
    self.assertIsNone(module.Class.method_58())
    self.assertIsNone(module.Class.method_59())
    self.assertIsNone(module.Class.method_60())
    self.assertIsNone(module.Class.method_61())
    self.assertIsNone(module.Class.method_62())
    self.assertIsNone(module.Class.method_63())
    self.assertIsNone(module.Class.method_64())
    self.assertIsNone(module.Class.method_65())
    self.assertIsNone(module.Class.method_66())
    self.assertIsNone(module.Class.method_67())
    self.assertIsNone(module.Class.method_68())
    self.assertIsNone(module.Class.method_69())
    self.assertIsNone(module.Class.method_70())
    self.assertIsNone(module.Class.method_71())
    self.assertIsNone(module.Class.method_72())
    self.assertIsNone(module.Class.method_73())
    self.assertIsNone(module.Class.method_74())
    self.assertIsNone(module.Class.method_75())
    self.assertIsNone(module.Class.method_76())
    self.assertIsNone(module.Class.method_77())
    self.assertIsNone(module.Class.method_78())
    self.assertIsNone(module.Class.method_79())
    self.assertIsNone(module.Class.method_80())
    self.assertIsNone(module.Class.method_81())
    self.assertIsNone(module.Class.method_82())
    self.assertIsNone(module.Class.method_83())
    self.assertIsNone(module.Class.method_84())
    self.assertIsNone(module.Class.method_85())
    self.assertIsNone(module.Class.method_86())
    self.assertIsNone(module.Class.method_87())
    self.assertIsNone(module.Class.method_88())
    self.assertIsNone(module.Class.method_89())
    self.assertIsNone(module.Class.method_90())
    self.assertIsNone(module.Class.method_91())
    self.assertIsNone(module.Class.method_92())
    self.assertIsNone(module.Class.method_93())
    self.assertIsNone(module.Class.method_94())
    self.assertIsNone(module.Class.method_95())
    self.assertIsNone(module.Class.method_96())
    self.assertIsNone(module.Class.method_97())
    self.assertIsNone(module.Class.method_98())
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