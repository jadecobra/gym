from utilities import POSITIONAL_ARGUMENTS, KEYWORD_ARGUMENTS

class Class(object):

    def method(self):
        return function()


class ClassA(object): pass


class ClassB(object): pass


class ClassC(object):
    attribute = None


class ClassD:

    @property
    def attribute(self):
        return 'attribute'

    @attribute.setter
    def attribute(self, value):
        pass


class ClassE:

    def __init__(self):
        self.attribute = None


class Container:

    def __init__(self):
        self.values = {}

    def __getitem__(self, name):
        return self.values[name]

    def __setitem__(self, name, value):
        self.values[name] = value

    def __delitem__(self, name):
        del self.values[name]

    def __iter__(self):
        return iter(self.values)


def function():
    return {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "keyN": "valueN",
    }

def function_with_positional_arguments(a, b, c):
    return function()