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
            self.assertIsNone(module.attribute_0)
    ```
    What is the code above doing?
    - `import unittest` imports the unittest module from the python standard library
    - `import module` import module from somewhere - this is going to hold the solution we write
    - `class TestAttributeError(unittest.TestCase):` - a class definition that inherits from `unittest.TestCase` and will hold our tests
    - `def test_defining_variables_to_solve_attribute_errors(self):` the definition of our first test function. we try to test one thing with our test function. In this case we are testing if definining variables can solve an `AttributeError`
    - `self.assertIsNone(module.attribute_0)` - the actual test. This is equivalent to asking the question `is module.attribute_0 equal to None`
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
    >       self.assertIsNone(module.attribute_0)
    E       AttributeError: module 'module' has no attribute 'attribute_0'

    tests/test_attribute_error.py:7: AttributeError
    ```
    Looking at the traceback starting from the bottom
    - `tests/test_attribute_error.py:7: AttributeError` the location and name of the Error that causes the failure
    - `E       AttributeError: module 'module' has no attribute 'attribute_0'` the module we imported has no definitions named `attribute_0`
    - `>       self.assertIsNone(module.attribute_0)` the line of code that errored out during execution
    - `def test_defining_variables_to_solve_attribute_errors(self):` the function definition where the error occurs
    - `self = <tests.test_attribute_error.TestAttributeError testMethod=test_defining_variables_to_solve_attribute_errors>` - A reference to the class and method(function) that caused the failure
- Open `module.py` in the Interactive Development Environment(IDE) and add the following
    ```python
    attribute_0
    ```
    The terminal will update to show the following
    ```shell
    tests/test_attribute_error.py:2: in <module>
        import module
    module.py:1: in <module>
        attribute_0
    E   NameError: name 'attribute_0' is not defined
    ```
    - `E   NameError: name 'attribute_0' is not defined` this is a new error so we add it to our running list of errors encountered. The running list now looks like this
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
            - A `NameError` occurs when there is a reference to name with no prior definition
        - What is similar between `ModuleNotFoundError`, `AttributeError` and `NameError`?
    - `attribute_0` the offending line
    - `module.py:1: in <module>` the location of the offending line
- Update `module.py` in the Interactive Development Environment(IDE) to
    ```python
    attribute_0 = None
    ```
    this explicity defines `attribute_0` with a value of `None` and the terminal updates to show a passing test. YES!!!
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
            self.assertIsNone(module.attribute_0)
            self.assertIsNone(module.attribute_1)
    ```
    the terminal will update to show an `AttributeError`
    ```shell
    >       self.assertIsNone(module.attribute_1)
    E       AttributeError: module 'module' has no attribute 'attribute_1'
    ```
#### <span style="color:green">**GREEN**</span>: Make it Pass
- <span style="color:red">**RED**</span>: Write a failing test - Update `module.py`
    ```python
    attribute_0 = None
    attribute_1
    ```
    the terminal will update to show a `NameError`
    ```shell
    module.py:2: in <module>
        attribute_1
    E   NameError: name 'attribute_1' is not defined
    ```
- <span style="color:green">**GREEN**</span>: Make it Pass - Update `module.py`
    ```python
    attribute_0 = None
    attribute_1 = None
    ```
    The terminal will update to show passing tests

#### <span style="color:red">**RED**</span>: Write a failing test
- Update `tests/test_attribute_error.py`
    ```python
    import unittest
    import module


    class TestAttributeError(unittest.TestCase):
        def test_defining_variables_to_solve_attribute_errors(self):
            self.assertIsNone(module.attribute_0)
            self.assertIsNone(module.attribute_1)
            self.assertIsNone(module.attribute_2)
    ```
    the terminal will update to show an `AttributeError`
    ```shell
    >       self.assertIsNone(module.attribute_2)
    E       AttributeError: module 'module' has no attribute 'attribute_2'
    ```
##### <span style="color:green">**GREEN**</span>: Make it Pass
- <span style="color:red">**RED**</span>: Write a failing test - Update `module.py`
    ```python
    attribute_0 = None
    attribute_1 = None
    attribute_2
    ```
    the terminal will update to show a `NameError`
    ```shell
    module.py:3: in <module>
        attribute_2
    E   NameError: name 'attribute_2' is not defined
    ```
- <span style="color:green">**GREEN**</span>: Make it Pass - Update `module.py`
    ```python
    attribute_0 = None
    attribute_1 = None
    attribute_2 = None
    ```
    The tests pass

##### <span style="color:red">**RED**</span>: Write a failing test
- Update `tests/test_attribute_error.py`
    ```python
    import unittest
    import module


    class TestAttributeError(unittest.TestCase):
        def test_defining_variables_to_solve_attribute_errors(self):
            self.assertIsNone(module.attribute_0)
            self.assertIsNone(module.attribute_1)
            self.assertIsNone(module.attribute_2)
            self.assertIsNone(module.attribute_3)
    ```
    the terminal will update to show an `AttributeError`
    ```shell
    >       self.assertIsNone(module.attribute_3)
    E       AttributeError: module 'module' has no attribute 'attribute_3'
    ```
##### <span style="color:green">**GREEN**</span>: Make it Pass
- <span style="color:red">**RED**</span>: Write a failing test - Update `module.py`
    ```python
    attribute_0 = None
    attribute_1 = None
    attribute_2 = None
    attribute_3
    ```
    the terminal will update to show a `NameError`
    ```shell
    module.py:4: in <module>
        attribute_3
    E   NameError: name 'attribute_3' is not defined
    ```
- <span style="color:green">**GREEN**</span>: Make it Pass - Update `module.py`
    ```python
    attribute_0 = None
    attribute_1 = None
    attribute_2 = None
    attribute_3 = None
    ```

This is the pattern. Update the `TestAttributeError` class in `tests/test_attribute_error.py` to add more tests
```python
def test_defining_variables_to_solve_attribute_errors(self):
    self.assertIsNone(module.attribute_0)
    self.assertIsNone(module.attribute_1)
    self.assertIsNone(module.attribute_2)
    self.assertIsNone(module.attribute_3)
    self.assertIsNone(module.attribute_4)
    self.assertIsNone(module.attribute_5)
    self.assertIsNone(module.attribute_6)
    self.assertIsNone(module.attribute_7)
    self.assertIsNone(module.attribute_8)
    self.assertIsNone(module.attribute_9)
    self.assertIsNone(module.attribute_10)
    self.assertIsNone(module.attribute_11)
    self.assertIsNone(module.attribute_12)
    self.assertIsNone(module.attribute_13)
    self.assertIsNone(module.attribute_14)
    self.assertIsNone(module.attribute_15)
    self.assertIsNone(module.attribute_16)
    self.assertIsNone(module.attribute_17)
    self.assertIsNone(module.attribute_18)
    self.assertIsNone(module.attribute_19)
    self.assertIsNone(module.attribute_20)
    self.assertIsNone(module.attribute_21)
    self.assertIsNone(module.attribute_22)
    self.assertIsNone(module.attribute_23)
    self.assertIsNone(module.attribute_24)
    self.assertIsNone(module.attribute_25)
    self.assertIsNone(module.attribute_26)
    self.assertIsNone(module.attribute_27)
    self.assertIsNone(module.attribute_28)
    self.assertIsNone(module.attribute_29)
    self.assertIsNone(module.attribute_30)
    self.assertIsNone(module.attribute_34)
    self.assertIsNone(module.attribute_32)
    self.assertIsNone(module.attribute_33)
    self.assertIsNone(module.attribute_34)
    self.assertIsNone(module.attribute_35)
    self.assertIsNone(module.attribute_36)
    self.assertIsNone(module.attribute_37)
    self.assertIsNone(module.attribute_38)
    self.assertIsNone(module.attribute_39)
    self.assertIsNone(module.attribute_40)
    self.assertIsNone(module.attribute_41)
    self.assertIsNone(module.attribute_42)
    self.assertIsNone(module.attribute_43)
    self.assertIsNone(module.attribute_44)
    self.assertIsNone(module.attribute_45)
    self.assertIsNone(module.attribute_46)
    self.assertIsNone(module.attribute_47)
    self.assertIsNone(module.attribute_48)
    self.assertIsNone(module.attribute_49)
    self.assertIsNone(module.attribute_50)
    self.assertIsNone(module.attribute_51)
    self.assertIsNone(module.attribute_52)
    self.assertIsNone(module.attribute_53)
    self.assertIsNone(module.attribute_54)
    self.assertIsNone(module.attribute_55)
    self.assertIsNone(module.attribute_56)
    self.assertIsNone(module.attribute_57)
    self.assertIsNone(module.attribute_58)
    self.assertIsNone(module.attribute_59)
    self.assertIsNone(module.attribute_60)
    self.assertIsNone(module.attribute_61)
    self.assertIsNone(module.attribute_62)
    self.assertIsNone(module.attribute_63)
    self.assertIsNone(module.attribute_64)
    self.assertIsNone(module.attribute_65)
    self.assertIsNone(module.attribute_66)
    self.assertIsNone(module.attribute_67)
    self.assertIsNone(module.attribute_68)
    self.assertIsNone(module.attribute_69)
    self.assertIsNone(module.attribute_70)
    self.assertIsNone(module.attribute_71)
    self.assertIsNone(module.attribute_72)
    self.assertIsNone(module.attribute_73)
    self.assertIsNone(module.attribute_74)
    self.assertIsNone(module.attribute_75)
    self.assertIsNone(module.attribute_76)
    self.assertIsNone(module.attribute_77)
    self.assertIsNone(module.attribute_78)
    self.assertIsNone(module.attribute_79)
    self.assertIsNone(module.attribute_80)
    self.assertIsNone(module.attribute_81)
    self.assertIsNone(module.attribute_82)
    self.assertIsNone(module.attribute_83)
    self.assertIsNone(module.attribute_84)
    self.assertIsNone(module.attribute_85)
    self.assertIsNone(module.attribute_86)
    self.assertIsNone(module.attribute_87)
    self.assertIsNone(module.attribute_88)
    self.assertIsNone(module.attribute_89)
    self.assertIsNone(module.attribute_90)
    self.assertIsNone(module.attribute_91)
    self.assertIsNone(module.attribute_92)
    self.assertIsNone(module.attribute_93)
    self.assertIsNone(module.attribute_94)
    self.assertIsNone(module.attribute_95)
    self.assertIsNone(module.attribute_96)
    self.assertIsNone(module.attribute_97)
    self.assertIsNone(module.attribute_98)
    self.assertIsNone(module.attribute_99)
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

    tests/test_attribute_error.py:11: AttributeError
    ```
    solving it the same way as the previous `AttributeError` we update `module.py`
    ```python
    ...
    function_0 = None
    ```
    the terminal updates to show
    ```shell
    >       self.assertIsNone(module.function_0())
    E       TypeError: 'NoneType' object is not callable

    tests/test_attribute_error.py:11: TypeError
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

    tests/test_attribute_error.py:12: AttributeError
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

    tests/test_attribute_error.py:15: AttributeError
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

    tests/test_attribute_error.py:15: TypeError
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

        tests/test_attribute_error.py:16: AttributeError
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
        - do we know how to define classes? so far our solution looks the same as defining functions

## How to solve the AttributeError by defining an Attribute in a Class

### <span style="color:red">**RED**</span>: Write a failing test

### <span style="color:green">**GREEN**</span>: Make it Pass

### <span style="color:orange">**REFACTOR**</span> - make it better

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

### <span style="color:green">**GREEN**</span>: Make it Pass

### <span style="color:orange">**REFACTOR**</span> - make it better

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