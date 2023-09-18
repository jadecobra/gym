# How to solve the IndentationError in python

We will step through solving an `IndentationError` in python using Test Driven Development

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

---

## Indentation Matters

Spacing/Indentation matters in python. Where you place code and how you space them out have an effect on how the code is interpreted as well as how a human being comprehends your intention.
Some people indent with 2 spaces, others indent with 4. In this exercise we will indent with 4.

## How to solve the IndentationError

### <span style="color:red">**RED**</span>: make it fail

- Open a new file in the editor and save it as `tests/test_indentation_error.py` in the `tests` folder you created in [Setup a Test Driven Development Environment](./TDD_SETUP.md) and type the following in the file. ***NOTE THE SPACING***

    ```python
    'a'
     'b'
    ```
    the terminal updates to show
    ```shell
    E       'b'
    E   IndentationError: unexpected indent
    ```
    add `IndentationError` to the running list of Exceptions encountered
    ```python
    # Exceptions Encountered
    # AssertionError
    # ModuleNotFoundError
    # AttributeError
    # NameError
    # TypeError
    # SyntaxError
    # IndentationError
    ```
    Why did line 2 create an error? python was not expecting the indentation there. Indentation has meaning in python and in this case it doesn't meet the predefined rules for indentation

### <span style="color:green">**GREEN**</span>: make it pass

- update `test_indentation_error.py`
    ```python
    'a'
    'b'
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's add more indentation errors to `test_indentation_error.py`
```python
'a'
'b'
    'c'
            'd'
```
The terminal updates to show
```shell
E       'c'
E   IndentationError: unexpected indent
```
fix the offending lines until all tests are green.

## How to solve the IndentationError for functions

Let's add more tests, this time indentation errors with functions, what's the difference in the spacing?

### <span style="color:red">**RED**</span>: make it fail

- update `test_indentation_error.py`
    ```python
    def function():
    pass

        def function():
        pass

     def function():
        pass

      def function():
        pass
    ```

### <span style="color:green">**GREEN**</span>: make it pass

- update `test_indentation_error.py` to make the spacing/indentation match
    ```python
    def function():
        pass

    def function():
        pass

    def function():
        pass

    def function():
        pass
    ```
    all the tests pass

## How to solve the IndentationError in Classes

Let's add more tests, this time indentation errors in Classes, what's the difference in the spacing?

### <span style="color:red">**RED**</span>: make it fail

- update `test_indentation_error.py`
    ```python
    class Class():
    pass

    class Class():
         pass

        class Class():
                pass
    ```
    the terminal will update to show an IndentationError and the offending line
    ```shell
    E    IndentationError: expected an indented block after class definition on line 18
    ```

### <span style="color:green">**GREEN**</span>: make it pass

- update `test_indentation_error.py` to make the spacing/indentation match
    ```python
    class Class():
        pass

    class Class():
        pass

    class Class():
        pass
    ```

## How to solve the IndentationError in Classes with Methods

### <span style="color:red">**RED**</span>: make it fail

- update `test_indentation_error.py`
    ```python
    class Class():
         def method():
        return

    class Class():
         def method():
             return

    class Class():
     def method():
         return
    ```
    the terminal will update to show an IndentationError and the offending line
    ```shell
    E    IndentationError: expected an indented block after function definition on line 28
    ```

### <span style="color:green">**GREEN**</span>: make it pass

- update `test_indentation_error.py` to make the spacing/indentation match
    ```python
    class Class():
        def method():
            return

    class Class():
        def method():
            return

    class Class():
        def method():
            return
    ```

## How to solve the IndentationError in Classes with Attributes

### <span style="color:red">**RED**</span>: make it fail

- update `test_indentation_error.py`
    ```python
    class Class():
     attribute = None
      attribute = None
           attribute = None
       attribute = None
    ```
    the terminal will update to show an IndentationError and the offending line
    ```shell
    E    IndentationError: unexpected indent
    ```

### <span style="color:green">**GREEN**</span>: make it pass

- update `test_indentation_error.py` to make the spacing/indentation match
    ```python
    class Class():
        attribute = None
        attribute = None
        attribute = None
        attribute = None
    ```

### <span style="color:orange">**REFACTOR**</span>: make it better

Is there anything we can do to make this better?
What was the point of this exercise?
Why does spacing matter and how many spaces should we use? some people use 2 some people use 4 and there is an argument over tabs versus spaces

It matters because python uses indentation to section off blocks of code.
When you define a function, all the statements that belong to the function are indented under the function.
When you define a class, all the statements that belong to the class include methods and attributes are indented under the class.
This helps with reading the code so you can tell what belongs to a name the same way curly braces do for languages that use them for that purpose.
Interactive Development Environments have gotten a lot better and tend to automatically indent for you so you don't have to spend time counting the number of spaces to indent when you create a function or class