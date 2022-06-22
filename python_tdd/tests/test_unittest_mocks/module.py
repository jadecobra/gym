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
        return 'something'

    @attribute.setter
    def attribute(self, value):
        pass


def function():
    return {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "keyN": "valueN",
    }

def function_with_positional_arguments(a, b, c):
    return function()