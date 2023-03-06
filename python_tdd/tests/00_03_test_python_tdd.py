import unittest
import module # Solve ModuleNotFoundError by creating module.py


class TestAttributeError(unittest.TestCase):

    '''
    AttributeError means there is a reference to something that does not exist

    you can create variables, functions, classes, attributes and methods to solve AttributeError
    '''

    def test_define_variables_to_solve_attribute_errors(self):
        self.assertIsNone(module.attribute)

    def test_defining_functions_to_solve_attribute_errors(self):
        self.assertIsNone(module.function())

    def test_defining_classes_to_solve_attribute_errors(self):
        self.assertIsInstance(module.Class(), object)

    def test_defining_attributes_in_classes_to_solve_attribute_errors(self):
        self.assertIsNone(module.Class.attribute)

    def test_defining_functions_in_classes_to_solve_attribute_errors(self):
        self.assertIsNone(module.Class.method())


class TestNameError(unittest.TestCase):

    '''
    AttributeError means there is a reference to something that does not exist

    you can create variables, functions, classes, attributes and methods to solve AttributeError
    '''

    def test_name_errors_for_variables(self):
        false
        true

        attribute_0

    def test_name_errors_for_functions(self):
        function()

    def test_name_errors_for_classes(self):
        Class()

    def test_name_errors_for_attributes(self):
        Class.attribute

    def test_name_errors_for_methods(self):
        Class.method()


class TestIdentationError(unittest.TestCase):

    '''
    IndentationError: your tabs and spaces do not match

    Make sure you use 4 spaces to indent
    '''

    def test_indentation_of_variables(self):
'a'
 'b'
    'c'
            'd'

    def test_indentation_of_functions(self):
        def function():
        pass

         def function():
            pass

    def test_indentation_of_classes(self):
         class Class():
        pass

        class Class():
       pass

    def test_indentation_of_attributes(self):
        class Class():
 attribute = None
  attribute = None
     attribute = None
   attribute = None

    def test_indentation_of_methods(self):
        class Class():
            def method():
            return

        class Class():
             def method():
                  return