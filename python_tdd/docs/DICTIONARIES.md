# Lists

We will cover `lists/arrays` in python using Test Driven Development

## Prerequisites

- [Setup a Test Driven Development Environment](./TDD_SETUP.md)

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

## How to create a Dictionary

Dictionaries/Mappings are key, value pairs that we can use to represent data. `values` can be any of the data structures above.

### <span style="color:red">**RED**</span>: make it fail

add a file named `test_dictionaries.py` to the `tests` folder

```python
import unittest
import dictionaries
```

the terminal updates to show a [ModuleNotFoundError](./MODULE_NOT_FOUND_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

add a file named `dictionaries.py` to the project folder and the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

- we will now proceed to look at the ways we can create a dictionary, add a failing test
    ```python


    class TestDictionaries(unittest.TestCase):

        def test_creating_dictionaries_with_strings_as_keys(self):
            self.assertEqual(dictionaries.a_dict(), {"key": "value"})
    ```
    the terminal updates to show an [AttributeError](./ATTRIBUTE_ERROR.md)
- add a definition for a function to `dictionaries.py`
    ```python
    def a_dict():
        return None
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md), our function returns `None` not a dictionary
- update the return statement to return an empty dictionary
    ```python
    def a_dict():
        return {}
    ```
    the terminal still shows an [AssertionError](./ASSERTION_ERROR.md) but now our return value looks more like what is expected
    ```python
    E       AssertionError: {} != {'key': 'value'}
    E       - {}
    E       + {'key': 'value'}
    ```
- update the return statement with the expected values
    ```python
    def a_dict():
        return {'key': 'value'}
    ```
    ***VOILA!*** The tests pass. You now know how to create a `dictionary`
- let's look at creating a dictionary with the `dict` keyword. add a test to `test_creating_dictionaries_with_strings_as_keys`
    ```python
    def test_creating_dictionaries_with_strings_as_keys(self):
        self.assertEqual(dictionaries.a_dict(), {'key': 'value'})
        self.assertEqual(dictionaries.a_dict(), dict(key='value'))
    ```
    the terminal shows passing tests, which means `dict(key='value')` and `{'key': 'value'}` produce the same results
- we can add another test just for fun, even though it is a repetition
    ```python
    def test_creating_dictionaries_with_strings_as_keys(self):
        self.assertEqual(dictionaries.a_dict(), {"key": "value"})
        self.assertEqual(dictionaries.a_dict(), dict(key='value'))
        self.assertEqual({"key": "value"}, dict(key='value'))
    ```

## How to create a dictionary with numbers as keys

### <span style="color:red">**RED**</span>: make it fail

add a failing test to `TestDictionaries`

```python
    def test_creating_dictionaries_with_numbers_as_keys(self):
        self.assertEqual({1: 'boom'}, {'one': 'boom'})
```

the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) since the two values are different

### <span style="color:green">**GREEN**</span>: make it pass

update the test to make it pass

```python
    def test_creating_dictionaries_with_numbers_as_keys(self):
        self.assertEqual({1: 'boom'}, {1: 'boom'})
```

the terminal updates to show passing tests

### <span style="color:orange">**REFACTOR**</span>: make it better

- Our knowledge of dictionaries is growing. We know we can use `strings` and `integers` as dictionary keys. Can we use floats? Let's add a test to check
    ```python
        def test_creating_dictionaries_with_numbers_as_keys(self):
            self.assertEqual({1: 'boom'}, {'one': 'boom'})
            self.assertEqual({2.5: 'works'}, {2.5: 'fails'})
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) as the values are different
- update the value on the right to make it pass
    ```python
    def test_creating_dictionaries_with_numbers_as_keys(self):
        self.assertEqual({1: 'boom'}, {'one': 'boom'})
        self.assertEqual({2.5: 'works'}, {2.5: 'works'})
    ```
    the terminal shows passing tests

## How to create a dictionary with booleans as keys

### <span style="color:red">**RED**</span>: make it fail

is it possible for us to use `False` or `True` as `dictionary` keys? Let's add a test to find out

```python
    def test_creating_dictionaries_with_booleans_as_keys(self):
        self.assertEqual({False: 'boom'}, {False: 'bap'})
```

the terminal shows an [AssertionError](./ASSERTION_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

update the return values to make them match and we are green again

```python
    def test_creating_dictionaries_with_booleans_as_keys(self):
        self.assertEqual({False: 'boom'}, {False: 'boom'})
```

### <span style="color:orange">**REFACTOR**</span>: make it better

- add a test for using `True` as a `dictionary` key
    ```python
    def test_creating_dictionaries_with_booleans_as_keys(self):
        self.assertEqual({False: 'boom'}, {False: 'boom'})
        self.assertEqual({True: 'bap'}, {True: 'boom'})
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md)
- update the values to make the tests pass
    ```python
    def test_creating_dictionaries_with_booleans_as_keys(self):
        self.assertEqual({False: 'boom'}, {False: 'boom'})
        self.assertEqual({True: 'bap'}, {True: 'bap'})
    ```

## How to create a dictionary with tuples as keys

### <span style="color:red">**RED**</span>: make it fail

add a test to `TestDictionaries`

```python
    def test_creating_dictionaries_with_tuples_as_keys(self):
        self.assertEqual({(1, 2): "value"}, {(1, 2): "key"})
```

the terminal shows an [AssertionError](./ASSERTION_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

we fix update the values to make it pass

```python
        self.assertEqual({(1, 2): "value"}, {(1, 2): "value"})
```

## Dictionary creation with lists, set, or dicts as keys

### <span style="color:red">**RED**</span>: make it fail

let's add a test to `TestDictionaries` using a list as a key

```python
    def test_creating_dictionaries_with_lists_as_keys(self):
        {[1, 2]: "BOOM"}
```

the terminal shows a [TypeError](./ASSERTION_ERROR.md) because only `hashable` types can be used as dictionary keys
```
E       TypeError: unhashable type: 'list'
```

### <span style="color:green">**GREEN**</span>: make it pass

like we learned in [Exception Handling](./EXCEPTION_HANDLING.md) we can add a `self.assertRaises` to confirm that creating a dictionary with a `list` as the key raises a [TypeError](./TYPE_ERROR.md)

```python
    def test_creating_dictionaries_with_lists_as_keys(self):
        with self.assertRaises(TypeError):
            {[1, 2]: "BOOM"}
```

all green here

### <span style="color:orange">**REFACTOR**</span>: make it better

- let's try the same using a set as a key
    ```python
    def test_creating_dictionaries_with_sets_as_keys(self):
        {{1, 2}: "BOOM"}
    ```
    the terminal shows a [TypeError](./ASSERTION_ERROR.md)
- we handle it
    ```python
    def test_creating_dictionaries_with_sets_as_keys(self):
        with self.assertRaises(TypeError):
            {{1, 2}: "BOOM"}
    ```
- what about creating a `dictionary` with a `dictionary` as a key
    ```python
    def test_creating_dictionaries_with_dictionaries_as_keys(self):
        a_dictionary = {"key": "value"}
        {a_dictionary: "BOOM"}
    ```
    the terminal shows a [TypeError](./TYPE_ERROR.md)
- we add a handler
    ```python
    def test_creating_dictionaries_with_dictionaries_as_keys(self):
        a_dictionary = {"key": "value"}
        with self.assertRaises(TypeError):
            {a_dictionary: "BOOM"}
    ```
    all tests pass

We now know that we can create dictionaries with the following [data structures](./DATA_STRUCTURES.md) as keys
- strings
- booleans
- integers
- floats
- tuples

## How to access dictionary values

We know how to create `dictionaries`, and what we can use as `keys`. How can we access values?
### <span style="color:red">**RED**</span>: make it fail

add a test to `TestDictionaries` in `test_dictionaries.py`

```python
    def test_accessing_dictionary_values(self):
        a_dictionary = {"key": "value"}
        self.assertEqual(a_dictionary["key"], "bob")
```

the terminal updates to show a failing test with an [AssertionError](./ASSERTION_ERROR.md) because `bob` is not equal to `value`

### <span style="color:green">**GREEN**</span>: make it pass

update the value to make the tests pass

```python
    def test_accessing_dictionary_values(self):
        self.assertEqual(a_dictionary["key"], "value")
```

the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

- we can also display the values of a dictionary as a list without the keys, add a test
    ```python
        def test_listing_dictionary_values(self):
            a_dictionary = {
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
                'keyN': 'valueN',
            }
            self.assertEqual(
                list(a_dictionary.values()), []
            )
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md)
- update the values to make the test pass
    ```python
    def test_listing_dictionary_values(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        self.assertEqual(
            list(a_dictionary.values()),
            ['value1', 'value2', 'value3', 'valueN']
        )
    ```
- we can do the same thing with the keys of the dictionary. let's add a test
    ```python
    def test_listing_dictionary_keys(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        self.assertEqual(
            list(a_dictionary.keys()),
            []
        )
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md)
- we update the test to make it pass
    ```python
    def test_listing_dictionary_keys(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        self.assertEqual(
            list(a_dictionary.keys()),
            ['key1', 'key2', 'key3', 'keyN']
        )
    ```

## How to get a value when the key does not exist

### <span style="color:red">**RED**</span>: make it fail

add a test

```python
    def test_dictionaries_raise_key_error_when_key_does_not_exist(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        a_dictionary['non_existent_key']
```

the terminal updates to show a [KeyError](https://docs.python.org/3/library/exceptions.html?highlight=keyerror#KeyError). A `KeyError` is raised when a `dictionary` is called with a `key` that does not exist.

### <span style="color:green">**GREEN**</span>: make it pass

- add `KeyError` to our running list of Exceptions Encountered
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
    # KeyError
    ```
- let's add an exception handler for the error like in [Exception Handling](./EXCEPTION_HANDLING.md)
    ```python
        def test_dictionaries_raise_key_error_when_key_does_not_exist(self):
            a_dictionary = {
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
                'keyN': 'valueN',
            }
            with self.assertRaises(KeyError):
                a_dictionary['non_existent_key']
    ```

### <span style="color:orange">**REFACTOR**</span>: make it better

What if we want to call a dictionary and not have an error? We could use the `get` function
- add a test to `TestDictionaries`
    ```python
    def test_how_to_get_a_value_when_a_key_does_not_exist(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        self.assertIsNone(a_dictionary['non_existent_key'])
    ```
    the terminal updates to show a `KeyError`
- update the test using the `get` method
    ```python
    def test_how_to_get_a_value_when_a_key_does_not_exist(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        self.assertIsNone(a_dictionary.get('non_existent_key'))
    ```
    the terminal updates to show a passing test. This means that when we use the `get` method and the `key` does not exist, we get `None` as the `return` value.
- let's state the above explicitly
    ```python
    def test_how_to_get_a_value_when_a_key_does_not_exist(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        self.assertIsNone(a_dictionary.get('non_existent_key'))
        self.assertIsNone(a_dictionary.get('non_existent_key', None))
    ```
    the terminal shows passing tests. The `get` method takes in 2 inputs
        - the `key`
        - the `value` it should return if the `key` does not exist
- based on what we know from [Exception Handling](./EXCEPTION_HANDLING.md) we can assume the definition of the [get](https://docs.python.org/3/library/stdtypes.html#dict.get) method looks something like this
    ```python
    def get(dictionary, key, default=None):
        try:
            return dictionary[key]
        except KeyError:
            return default
    ```
- let's try the `get` method with an existing key
    ```python
    def test_how_to_get_a_value_when_a_key_does_not_exist(self):
        a_dictionary = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
            'keyN': 'valueN',
        }
        self.assertIsNone(a_dictionary.get('non_existent_key'))
        self.assertIsNone(a_dictionary.get('non_existent_key', None))
        self.assertEqual(a_dictionary.get('key1', None), None)
    ```
    the terminal updates to show an [Assertion Error](./ASSERTION_ERROR.md) because `value1` is not equal to `None`
- update the test to make it pass

## How to view the attributes and methods of a dictionary

[CLASSES] covers how to view the `attributes` and `methods` of an object. Let's do the same for `dictionaries`

### <span style="color:red">**RED**</span>: make it fail

add a test to `TestDictionaries`

```python
    def test_dictionary_attributes(self):
        self.maxDiff = None
        self.assertEqual(
            dir(dictionaries.a_dict()),
            []
        )
```

the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

update the test with the expected values

```python
    def test_dictionary_attributes(self):
        self.maxDiff = None
        self.assertEqual(
            dir(dictionaries.a_dict()),
            [
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
                '__init__',
                '__init_subclass__',
                '__ior__',
                '__iter__',
                '__le__',
                '__len__',
                '__lt__',
                '__ne__',
                '__new__',
                '__or__',
                '__reduce__',
                '__reduce_ex__',
                '__repr__',
                '__reversed__',
                '__ror__',
                '__setattr__',
                '__setitem__',
                '__sizeof__',
                '__str__',
                '__subclasshook__',
                'clear',
                'copy',
                'fromkeys',
                'get',
                'items',
                'keys',
                'pop',
                'popitem',
                'setdefault',
                'update',
                'values'
            ]
        )
```

the tests pass

### <span style="color:orange">**REFACTOR**</span>: make it better

We see some of the methods we have covered so far and others we did not. You can write tests on the others to discover what they do and/or [read more about dictionaries](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict). Let's list out what we know so far and you can fill in the others as you learn them
- clear
- copy
- fromkeys
- get - gets the `value` for a `key` and returns a default value/None if the key does not exist
- items
- keys - returns the list of `keys` in a dictionary
- pop
- popitem
- setdefault
- update
- values - returns the list of `values` in a dictionary

## How to set a default value for a given key

Let's test the `setdefault` method

### <span style="color:red">**RED**</span>: make it fail

add a test

```python
    def test_set_default_for_a_given_key(self):
        a_dictionary = {'bippity': 'boppity'}
        a_dictionary['another_key']
```

the terminal updates to show a `KeyError`

### <span style="color:green">**GREEN**</span>: make it pass

add a `self.assertRaises` to confirm that the `KeyError` gets raised and make the test pass

```python
    def test_set_default_for_a_given_key(self):
        a_dictionary = {'bippity': 'boppity'}

        with self.assertRaises(KeyError):
            a_dictionary['another_key']
```

### <span style="color:orange">**REFACTOR**</span>: make it better

- add a test for `setdefault`
    ```python
    def test_set_default_for_a_given_key(self):
        a_dictionary = {'bippity': 'boppity'}

        with self.assertRaises(KeyError):
            a_dictionary['another_key']

        a_dictionary.setdefault('another_key')
        self.assertEqual(a_dictionary, {'bippity': 'boppity'})
    ```
    the terminal updates to show that `a_dictionary` has changed. It has a new key which was not there before
- update the test to make it pass
    ```python
    def test_set_default_for_a_given_key(self):
        a_dictionary = {'bippity': 'boppity'}

        with self.assertRaises(KeyError):
            a_dictionary['another_key']

        a_dictionary.setdefault('another_key')
        self.assertEqual(a_dictionary, {'bippity': 'boppity', 'another_key': None})
    ```
- What if we want to add a `key` but set the default value to something other than `None`? Good question, Let's add a test to find out
    ```python
        a_dictionary.setdefault('a_new_key', 'a_default_value')
        self.assertEqual(a_dictionary, {'bippity': 'boppity', 'another_key': None})
    ```
    the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) since `a_dictionary` now has a new `key` and `value`
- update the test to make it pass
    ```python
        self.assertEqual(
            a_dictionary,
            {
                'bippity': 'boppity',
                'another_key': None,
                'a_new_key': 'a_default_value',
            }
        )
    ```
    all tests pass, and we update the list of methods with what we now know about `setdefault`

## How to update a Dictionary with another dictionary

What if we have a dictionary and want to `add` the `keys` and `values` of another dictionary to it?

### <span style="color:red">**RED**</span>: make it fail

add a test to `TestDictionaries`

```python
    def test_adding_two_dictionaries(self):
        a_dictionary = {
            "basic": "toothpaste",
            "whitening": "peroxide",
        }
        a_dictionary.update({
            "non_basic": "chewing stick",
            "browning": "tobacco",
            "decaying": "sugar"
        })
        self.assertEqual(
            a_dictionary,
            {"basic": "toothpaste", "whitening": "peroxide"}
        )
```

the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md) because the values of `a_dictionary` where updated when we called the `update` method on it

### <span style="color:green">**GREEN**</span>: make it pass

update values to make it pass

## How to remove an item from a dictionary

We can remove an item from a dictionary with the `pop` method. It deletes

### <span style="color:red">**RED**</span>: make it fail

add a failing test to `TestDictionaries`

```python
    def test_pop(self):
        a_dictionary = {
            "basic": "toothpaste",
            "whitening": "peroxide",
            "non_basic": "chewing stick",
            "browning": "tobacco",
            "decaying": "sugar"
        }
        self.assertEqual(a_dictionary.pop("basic"), None)
```

the terminal updates to show an [AssertionError](./ASSERTION_ERROR.md)

### <span style="color:green">**GREEN**</span>: make it pass

update the test with the right value to make it pass

### <span style="color:orange">**REFACTOR**</span>: make it better

