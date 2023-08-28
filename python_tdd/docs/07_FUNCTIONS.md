# How to write functions in python

This tutorial will step through functions in python using Test Driven Development

## Prerequisites

- [Setup Test Driven Development Project](./TDD_SETUP.md)

---

## Functions

`functions` are a callable unit/block of code. It is a way we can encapsulate statements that we can use later to do some task.
With functions we make code modular which makes it easier to test and reuse.

## How to define functions

We define `functions` with the `def` keyword

## <span style="color:red">**RED**</span>: make it fail

create a file named `test_functions.py` in the `tests` folder and add the following

```python
import unittest
import functions


class TestFunctions(unittest.TestCase):

    def test_functions_with_pass(self):
        self.assertIsNone(functions.function_with_pass())
```

the terminal updates to show an `AttributeError`. We played with those in [01_TDD_ATTRIBUTE_ERROR](./01_ATTRIBUTE_ERROR.md)

## <span style="color:green">**GREEN**</span>: make it pass

update `functions.py` with a function definition
```python
    def function_with_pass():
        pass
```
the test passes. Why?
- the test checks if the value of the call to `functions.function_with_pass` is `None`
- the function definition simply says `pass` yet the test passes
- why does it pass? In python all functions return `None` by default, imagine the function has an invisible line that says `return None`

## <span style="color:orange">**REFACTOR**</span>: make it better

Let's test if functions really always return `None` by default

### <span style="color:red">**RED**</span>: make it fail

add a new test to `TestFunctions` in `test_functions.py`

```python
    def test_functions_with_return(self):
        self.assertIsNone(functions.function_with_return())
```
the terminal updates to show an `AttributeError`

### <span style="color:green">**GREEN**</span>: make it pass

update `functions.py` to make the test pass
```python
    def function_with_return(self):
        return
```
why does this also pass? we have defined 2 functions with different statements in their body but we get the same result. In python all functions return `None` by default, imagine the function has an invisible line that says `return None`

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's add one more test

### <span style="color:red">**RED**</span>: make it fail

update `TestFunctions` in `test_functions.py`

```python
    def test_functions_with_return_none(self):
        self.assertIsNone(functions.function_with_return_none())
```
the terminal updates to show an `AttributeError`

### <span style="color:green">**GREEN**</span>: make it pass

update `functions.py` with a function definition

```python
def function_with_return_none():
    return None
```
and the terminal updates to show passing tests.
- We can safely say that the 3 ways we just defined the function have the exact same outcome. They all return `None`
- If they all return None, why are they written differently?

***A LITTLE NOTE ON FUNCTIONS***
> - `pass` is a placeholder, it has no action but keeps our code syntactically correct while we figure out what to put there
> - `return` implies `return None`, because `return` gives whatever value is given after the keyword and since no value is given and `None` represents no value...
> - `return None` explicitly states what it is returning. What do you think of writing functions this way so that the reader always knows exactly what the function is returning?

### <span style="color:orange">**REFACTOR**</span>: make it better

Here's what we know so far about functions in python
- functions are defined using the `def` keyword
- functions return `None` by default

## Passthrough Functions

What else can we do with functions? We know a function can produce/return an output, and it can take in an input. As a simple test let's create a passthrough function.
What is a passthrough function? A function that returns the input given

### <span style="color:red">**RED**</span>: make it fail

update `TestFunctions` in `test_functions.py`

```python
    def test_passthrough_function(self):
        self.assertEqual(functions.passthrough(False), False)
```
the terminal updates to show an `AttributeError`

### <span style="color:green">**GREEN**</span>: make it pass

- update `functions.py` with a function definition
    ```python
    def passthrough():
        return None
    ```
    the terminal updates to show a `TypeError`
    ```python
    TypeError: passthrough() takes 0 positional arguments but 1 was given
    ```
- update `passthrough` in `functions.py` to take 1 positional argument
    ```python
    def passthrough(input_data):
        return None
    ```
    the terminal updates to show an `AssertionError`
    ```python
    AssertionError: None != False
    ```
    because the result of `functions.passthrough(False)` is `None` which is not equal to `False`
- update `passthrough` to make the test pass
    ```python
    def passthrough(input_data):
        return False
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

Wait a minute. Something is not quite right here. The definition for a passthrough function was that it returned the same thing it was given, our test passes when `False` is given but will it still pass when another value is given as the input or will it always return `False`? Let's test it

#### <span style="color:red">**RED**</span>: make it fail

update `test_passthrough_function` in `TestFunctions` with a new test
```python
    def test_passthrough_function(self):
        self.assertEqual(functions.passthrough(False), False)
        self.assertEqual(functions.passthrough(True), True)
```
the terminal updates to show an `AssertionError`
```python
AssertionError: False != True
```
How can we make it pass?

#### <span style="color:green">**GREEN**</span>: make it pass

update the definition of `passthrough` in `functions.py`
```python
def passthrough(input_data):
    return input_data
```
the terminal updates to show passing tests. We have more confidence that our passthrough function will likely return the input data it is given. Let's add more tests to be sure

#### <span style="color:orange">**REFACTOR**</span>: make it better

update `test_passthrough_function`
```python
    def test_passthrough_function(self):
        self.assertEqual(functions.passthrough(False), False)
        self.assertEqual(functions.passthrough(True), True)
        self.assertEqual(functions.passthrough(None), False)
        self.assertEqual(functions.passthrough(int), False)
        self.assertEqual(functions.passthrough(str), False)
        self.assertEqual(functions.passthrough(tuple), False)
        self.assertEqual(functions.passthrough(list), False)
        self.assertEqual(functions.passthrough(set), False)
        self.assertEqual(functions.passthrough(dict), False)
```
the terminal updates to show `AssertionError` for each line until we make the input match the output, proving that the passthrough function we have defined returns the input it is given

## Functions with positional arguments

What if we want our function to take in more than one input? For instance if we are writing a function to add 2 numbers, it has to be able to accept the 2 numbers it is adding

### <span style="color:red">**RED**</span>: make it fail

update `test_functions.py` with a new test, replacing `my_first_name` and `my_last_name` with your first and last names
```python
    def test_functions_with_positional_arguments(self):
        self.assertEqual(
            functions.passthrough_with_positional_arguments('my_first_name', 'my_last_name'),
            ('my_first_name', 'my_last_name')
        )
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- update `functions.py` with the solution we know works from `test_passthrough_function`
    ```python
    def test_passthrough_with_positional_arguments(input_data):
        return input_data
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md)
- update the signature of `passthrough_with_positional_arguments` to take in more than one argument
    ```python
    def passthrough_with_positional_arguments(input_data, second_argument):
        return input_data
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update `passthrough_with_positional_arguments` to return the two arguments it receives
    ```python
    def passthrough_with_positional_arguments(input_data, second_argument):
        return input_data, second_argument
    ```
    the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

How can we make this better?
- we named the first argument `input_data` and the second argument `second_argument`. Technically, both arguments are input data, so we need a better name that is more descriptive
- update `passthrough_with_positional_arguments` to use more descriptive names
    ```python
    def passthrough_with_positional_arguments(first_argument, second_argument):
        return first_argument, second_argument
    ```
    the terminal still shows passing tests
- let's add another test to ensure that it outputs data in the order given. update `test_functions_with_positional_arguments`
    ```python
    self.assertEqual(
        functions.passthrough_with_positional_arguments('my_last_name', 'my_first_name'),
        ('my_first_name', 'my_last_name')
    )
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the test to the correct output
    ```python
    self.assertEqual(
        functions.passthrough_with_positional_arguments('my_last_name', 'my_first_name'),
        ('my_last_name', 'my_first_name')
    )
    ```
    the terminal updates to show passing tests
- our function only takes in 2 positional arguments
    - how do we take in 2 or more positional arguments?
    - what do we do if we do not know the number of positional arguments that will be given?
- let's update `test_functions_with_positional_arguments` to add tests for these cases
    ```python
    self.assertEqual(
        functions.passthrough_with_positional_arguments(0, 1, 2, 3),
        (0, 1, 2, 3)
    )
    self.assertEqual(
        functions.passthrough_with_positional_arguments(bool, int, float, str, tuple, list, set, dict),
        (bool, int, float, str, tuple, list, set, dict)
    )
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md) because 2 positional arguments were expected by the function but 4 were given
- update the signature of `functions_with_positional_arguments` with a starred expression to take in any number of arguments
    ```python
    def passthrough_with_positional_arguments(*arguments):
        return arguments
    ```
    the terminal updates to show passing tests. But wait, what is a starred expression? it is a way to represent multiple arguments with one. For now we trust in the evidence that it works, until we understand it better

## Functions with keyword arguments

There is an inherent problem with using positional arguments in functions. It requires the input data to always be supplied in the correct sequence. If our program is dependent on that sequence, then we will have a problem. How do we ensure that the arguments given are always the arguments intended? How do we make sure that our function behaves correctly regardless of what order the user provides the input data?

We can name our arguments, that way the function no longer cares about the order

### <span style="color:red">**RED**</span>: make it fail

add a new test to `test_functions.py`
```python
    def test_functions_with_keyword_arguments(self):
        self.assertEqual(
            functions.passthrough_with_keyword_arguments(
                first_name='my_first_name',
                last_name='my_last_name'
            ),
            ('my_first_name', 'my_last_name')
        )
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- update `functions.py` with a function definition
    ```python
    def passthrough_with_keyword_arguments():
        return None
    ```
    the terminal updates to show
    ```python
    TypeError: passthrough_with_keyword_arguments() got an unexpected keyword argument 'first_name'
    ```
- update the function signature to take in a positional argument
    ```python
    def passthrough_with_keyword_arguments(first_name):
        return None
    ```
    the terminal updates to show
    ```python
    TypeError: passthrough_with_keyword_arguments() got an unexpected keyword argument 'last_name'
    ```
- update the function to take in another positional argument
    ```python
    def passthrough_with_keyword_arguments(first_name, last_name):
        return None
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the return statement to make the test pass
    ```python
    def passthrough_with_keyword_arguments(first_name, last_name):
        return first_name, last_name
    ```
    Eureka! the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

So far `passthrough_with_keyword_arguments` looks the same as `passthrough_with_positional_arguments` did when it took in 2 positional arguments, so what's the difference between a positional argument and a keyword argument?

- add a test that puts the input data out of order to see if there's a difference
    ```python
        self.assertEqual(
            functions.passthrough_with_keyword_arguments(
                last_name='my_last_name',
                first_name='my_first_name'
            ),
            ('my_first_name', 'my_last_name')
        )
    ```
    the terminal updates to show passing tests. Unlike in `test_functions_with_positional_arguments` using the name makes sure that the function always displays the output in the right order regardless of the order the input data is given
- this function only takes in 2 keyword arguments. what if we wanted a function that can take in any number of keyword arguments? There is a starred expression for keyword arguments. It uses `**`.

### <span style="color:red">**RED**</span>: make it fail
Let's add a test to `test_functions_with_keyword_arguments`
```python
    self.assertEqual(
        functions.passthrough_with_keyword_arguments(
            a=1, b=2, c=3, d=4
        ),
        {}
    )
```
the terminal updates to show a [TypeError](./03_TYPE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

- update the signature for `passthrough_with_keyword_arguments` to accept any number of keyword arguments
    ```python
    def passthrough_with_keyword_arguments(**keyword_arguments):
        return keyword_arguments
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for our previous test that was passing. We have introduced a regression
- update `test_functions_with_keyword_arguments` to the updated output
    ```python
    self.assertEqual(
        functions.passthrough_with_keyword_arguments(
            first_name='my_first_name',
            last_name='my_last_name'
        ),
        {'first_name': 'my_first_name', 'last_name': 'my_last_name'}
    )
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the next test that was passing. Still a regression
- update the next test to make the output more appropriate
    ```python
    self.assertEqual(
        functions.passthrough_with_keyword_arguments(
            last_name='my_last_name',
            first_name='my_first_name'
        ),
        {'first_name': 'my_first_name', 'last_name': 'my_last_name'}
    )
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md) for the last test we added.
- update the test to the expected value in the comparison
    ```python
    self.assertEqual(
        functions.passthrough_with_keyword_arguments(
            a=1, b=2, c=3, d=4
        ),
        {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    )
    ```
    the terminal updates to show passing tests. We now know that keyword arguments are treated as [Dictionaries](./09_DICTIONARIES.md) in python

### <span style="color:orange">**REFACTOR**</span>: make it better

Let's add one more test for good measure
- update `test_functions_with_keyword_arguments`
    ```python
    self.assertEqual(
        functions.passthrough_with_keyword_arguments(
            a_boolean=bool,
            an_integer=int,
            a_float=float,
            a_string=str,
            a_tuple=tuple,
            a_list=list,
            a_set=set,
            a_dictionary=dict
        ),
        {}
    )
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the test with the right values to make the test pass
    ```python
    self.assertEqual(
        functions.passthrough_with_keyword_arguments(
            a_boolean=bool,
            an_integer=int,
            a_float=float,
            a_string=str,
            a_tuple=tuple,
            a_list=list,
            a_set=set,
            a_dictionary=dict
        ),
        {
            'a_boolean': bool,
            'an_integer': int,
            'a_float': float,
            'a_string': str,
            'a_tuple': tuple,
            'a_list': list,
            'a_set': set,
            'a_dictionary': dict
        }
    )
    ```
    the terminal updates to show passing tests

## Functions with positional and keyword arguments

What if we want to define a function that can take in both positional and keyword arguments?

### <span style="color:red">**RED**</span>: make it fail

how can we write a test for a function that accepts positional and keyword arguments?
- we know how to write a function that takes positional arguments
- we know how to write a function that takes keyword arguments
- add a test to `test_functions.py`
    ```python
        def test_functions_with_positional_and_keyword_arguments(self):
            self.assertEqual(
                functions.accepts_positional_and_keyword_arguments(last_name='my_last_name', 'my_first_name'),
                {}
            )
    ```
    the terminal updates to show a `SyntaxError` because we put a positional argument after a keyword argument

### <span style="color:green">**GREEN**</span>: make it pass

- fix the order of arguments in `test_functions_with_positional_and_keyword_arguments`
    ```python
    self.assertEqual(
        functions.accepts_positional_and_keyword_arguments('my_first_name', last_name='my_last_name'),
        {}
    )
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- add a definition for the function to `functions.py`
    ```python
    def accepts_positional_and_keyword_arguments():
        return None
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md)
    ```python
     TypeError: accepts_positional_and_keyword_arguments() got an unexpected keyword argument 'last_name'
    ```
- how do we update the function signature to accept a keyword argument?
    ```python
    def accepts_positional_and_keyword_arguments(last_name):
        return None
    ```
    the terminal updates to show another [TypeError](./03_TYPE_ERROR.md)
    ```python
    TypeError: accepts_positional_and_keyword_arguments() got multiple values for argument 'last_name'
    ```
- update the function signature to accept another argument
    ```python
    def accepts_positional_and_keyword_arguments(last_name, first_name):
        return None
    ```
    the terminal shows the same error even though we have 2 different arguments. How can we let the program know which argument is positional and which is a keyword argument?
- What happens if we reorder the arguments?
    ```python
    def accepts_positional_and_keyword_arguments(first_name, last_name):
        return None
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
- update the return statement to make the test pass
    ```python
    def accepts_positional_and_keyword_arguments(first_name, last_name):
        return first_name, last_name
    ```
    the terminal updates the [AssertionError](./04_ASSERTION_ERROR.md) with the values we just added
- update `test_functions_with_positional_and_keyword_arguments` to make our results match the expectation
    ```python
    def test_functions_with_positional_and_keyword_arguments(self):
        self.assertEqual(
        functions.accepts_positional_and_keyword_arguments('my_first_name', last_name='my_last_name'),
        ('my_first_name', 'my_last_name')
    )
    ```
    the terminal shows passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

Hold on a second. This looks exactly like what we did in `test_functions_with_positional_arguments`
- How do we know from the function signature which argument is positional and which is a keyword argument?
- Is there a way to specify explicitly without waiting for the function to fail when we send in values?
- update `accepts_positional_and_keyword_arguments` to have a default value for the keyword argument
    ```python
    def accepts_positional_and_keyword_arguments(first_name, last_name=None):
        return first_name, last_name
    ```
    all tests are still passing
- why didn't we add a default argument for `first_name`? What would happen if we did? Let's test it
    ```python
    def accepts_positional_and_keyword_arguments(first_name=None, last_name=None):
        return first_name, last_name
    ```
    it looks like python lets us use default arguments with no issues, and we can provide keyword arguments positionally without using the keyword. Let's add another test to prove this
- add a test to `test_functions_with_positional_and_keyword_arguments`
    ```python
    self.assertEqual(
        functions.accepts_positional_and_keyword_arguments('my_first_name', 'my_last_name'),
        ('my_first_name', 'my_last_name')
    )
    ```
    all the tests are still passing. The problem here is without the names the program is going to take the input data in the order we provide it so it is better to be explicit with the names.
- let's add another test, this time with an unknown number of parameters and keyword arguments
    ```python
    self.assertEqual(
        functions.accepts_positional_and_keyword_arguments(
            bool, int, float, str, tuple, list, set, dict,a_boolean=bool, an_integer=int, a_float=float,a_string=str, a_tuple=tuple, a_list=list, a_set=set,
                a_dictionary=dict
            ),
        ()
    )
    ```
    the terminal updates to show a [TypeError](./03_TYPE_ERROR.md) because the function signature specifically only has two keyword arguments which are not provided in the call
- using what we know from previous tests we update the function using starred expressions
    ```python
    def accepts_positional_and_keyword_arguments(*args, **kwargs):
        return args, kwargs
    ```
    the terminal updates to show a failure for a previous passing test
    ```python
        def test_functions_with_positional_and_keyword_arguments(self):
    >       self.assertEqual(
                functions.accepts_positional_and_keyword_arguments('my_first_name', last_name='my_last_name'),
                ('my_first_name', 'my_last_name')
            )
    E       AssertionError: Tuples differ: (('my_first_name',), {'last_name': 'my_last_name'}) != ('my_first_name', 'my_last_name')
    ```
- comment out the other tests so we can focus on the failing test
    ```python
    def test_functions_with_positional_and_keyword_arguments(self):
        self.assertEqual(
            functions.accepts_positional_and_keyword_arguments('my_first_name', last_name='my_last_name'),
            ('my_first_name', 'my_last_name')
        )
        # self.assertEqual(
        #     functions.accepts_positional_and_keyword_arguments('my_first_name', 'my_last_name'),
        #     (('my_first_name', 'last_name'), {})
        # )
        # self.assertEqual(
        #     functions.accepts_positional_and_keyword_arguments(),
        #     (None, None)
        # )
        # self.assertEqual(
        # functions.accepts_positional_and_keyword_arguments(
        #     bool, int, float, str, tuple, list, set, dict,a_boolean=bool, an_integer=int, a_float=float,a_string=str, a_tuple=tuple, a_list=list, a_set=set,
        #     a_dictionary=dict
        #     ),
        #     ()
        # )
    ```
- update the test to make it pass
    ```python
        self.assertEqual(
            functions.accepts_positional_and_keyword_arguments('my_first_name', last_name='my_last_name'),
            (('my_first_name',), {'last_name': 'my_last_name'})
        )
    ```
    the terminal updates to show tests passing
- uncomment the next test
    ```python
            self.assertEqual(
            functions.accepts_positional_and_keyword_arguments('my_first_name', 'my_last_name'),
            (('my_first_name', 'last_name'), {})
        )
    ```
    the terminal updates to show
    ```python
    >       self.assertEqual(
                functions.accepts_positional_and_keyword_arguments('my_first_name', 'my_last_name'),
                (('my_first_name', 'last_name'), {})
            )
    E       AssertionError: Tuples differ: (('my_first_name', 'my_last_name'), {}) != (('my_first_name', 'last_name'), {})
    ```
- update the test to make it pass
    ```python
    self.assertEqual(
            functions.accepts_positional_and_keyword_arguments('my_first_name', 'my_last_name'),
            (('my_first_name', 'my_last_name'), {})
        )
    ```
    the terminal updates to show passing tests
- uncomment the next test to see it fail
    ```python
        self.assertEqual(
            functions.accepts_positional_and_keyword_arguments(),
            (None, None)
        )
    ```
    the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
    ```python
    AssertionError: Tuples differ: ((), {}) != (None, None)
    ```
- update the test to make it pass
    ```python
        self.assertEqual(
            functions.accepts_positional_and_keyword_arguments(),
            ((), {})
        )
    ```
- uncomment the last test to see it fail and the terminal updates to show an [AssertionError](./04_ASSERTION_ERROR.md)
    ```python
    AssertionError: Tuples differ: ((<class 'bool'>, <class 'int'>, <class 'f[307 chars]t'>}) != ()
    ```
- update the test to make it pass
    ```python
    self.assertEqual(
            functions.accepts_positional_and_keyword_arguments(
                bool, int, float, str, tuple, list, set, dict,a_boolean=bool, an_integer=int, a_float=float,a_string=str, a_tuple=tuple, a_list=list, a_set=set,
                a_dictionary=dict
            ),
            (
                (bool, int, float, str, tuple, list, set, dict,),
                {
                    'a_boolean': bool,
                    'an_integer': int,
                    'a_float': float,
                    'a_string': str,
                    'a_tuple': tuple,
                    'a_list': list,
                    'a_set': set,
                    'a_dictionary': dict
                }
            )
        )
    ```
    the terminal updates to show passing tests
- From what we have seen so far, in python
    - positional arguments are represented as `tuples`
    - keyword arguments are represented as `dictionaries`
    - we can use `*name` to represent any number of positional arguments
    - we can use `**name` to represent any number of keyword arguments
    - we can define default values for arguments
    - positional arguments must come before keyword arguments

## Singleton Functions

A singleton function is a function that returns the exact same thing every time it is called, regardless of input.

### <span style="color:red">**RED**</span>: make it fail

add a test to `test_functions.py`
```python
    def test_singleton_function(self):
        self.assertEqual(functions.singleton(), 'my_first_name')
```
the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

update `functions.py` to make it pass
```python
def singleton():
    return 'my_first_name'
```

### <span style="color:orange">**REFACTOR**</span>: make it better

add a new test that checks if a singleton that accepts inputs returns the same value when it is given inputs

- update `test_functions.py`
    ```python
    def test_singleton_function_with_input(self):
        self.assertEqual(functions.singleton_with_input('Bob', 'James', 'Frank'), 'joe')
        self.assertEqual(functions.singleton_with_input('a', 2, 'c', 3), 'joe')
    ```
    the terminal updates to show an [AttributeError](./01_ATTRIBUTE_ERROR.md)
- update `singleton_with_inputs` to make the test pass
    ```python
    def singleton_with_inputs(*args):
        return 'joe'
    ```

***WELL DONE!***
> You now know
> - how to write functions in python that can take in any number of positional or keyword arguments as inputs
> - positional arguments are represented as `tuples`
> - keyword arguments are represented as `dictionaries`
> - we can use `*name` to represent any number of positional arguments
> - we can use `**name` to represent any number of keyword arguments
> - we can define default values for arguments
> - positional arguments must come before keyword arguments
> - singleton functions return the same thing everytime they are called

Do you want to read more about
- [functions](https://docs.python.org/3/glossary.html#term-function)
- [methods](https://docs.python.org/3/glossary.html#term-method)
- [parameters](https://docs.python.org/3/glossary.html#term-parameter)
- [function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
- [nested scope](https://docs.python.org/3/glossary.html#term-nested-scope)