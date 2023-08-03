# How to solve the IndentationError in Python

This tutorial will step through solving an `IndentationError` in Python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Indentation Matters

Spacing/Indentation matters in Python. Where you place code and how you space them out have an effect on how the code is interpreted as well as how a human being comprehends your intention.
Some people indent with 2 spaces, others indent with 4. In this exercise we will indent with 4.

## How to solve the IndentationError

### <span style="color:red">**RED**</span>: Write a failing test

- Open a new file in the editor and save it as `tests/test_indentation_error.py` in the `tests` folder you created in [Setup Test Driven Development Project](./TDD_SETUP.md) and type the following in the file. ***NOTE THE SPACING***

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
    ```
    Why did line 2 create an error? Python was not expecting the indentation there. Indentation has meaning in Python and in this case it doesn't meet the predefined rules for indentation

### <span style="color:green">**GREEN**</span>: Make it Pass

- update `test_indentation_error.py`
    ```python
    'a'
    'b'
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span> - make it better

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

### <span style="color:red">**RED**</span>: Write a failing test

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

### <span style="color:green">**GREEN**</span>: Make it Pass

- update `test_indentation_error.py` to make the spacing match
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
