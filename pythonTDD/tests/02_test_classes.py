import unittest
import classes
import datetime


class TestClasses(unittest.TestCase):
    def test_class_definitions_with_pass(self):
        self.assertIsInstance(classes.ClassWithPass(), object)

    def test_class_definitions_with_parentheses(self):
        self.assertIsInstance(classes.ClassWithParentheses(), object)

    def test_class_definition_with_object(self):
        self.assertIsInstance(classes.ClassWithObject(), object)

    def test_classes_with_attributes(self):
        self.assertEqual(classes.ClassWithAttributes.attribute_a, "AttributeA")
        self.assertEqual(classes.ClassWithAttributes.attribute_b, "AttributeB")
        self.assertEqual(classes.ClassWithAttributes.attribute_c, "AttributeC")
        self.assertEqual(classes.ClassWithAttributes.attribute_d, "AttributeD")

    def test_classes_with_methods(self):
        self.assertEqual(classes.ClassWithMethods.method_a(), "You called MethodA")
        self.assertEqual(classes.ClassWithMethods.method_b(), "You called MethodB")
        self.assertEqual(classes.ClassWithMethods.method_c(), "You called MethodC")
        self.assertEqual(classes.ClassWithMethods.method_d(), "You called MethodD")

    def test_classes_with_attributes_and_methods(self):
        self.assertEqual(classes.ClassWithAttributesAndMethods.attribute, "Attribute")
        self.assertEqual(
            classes.ClassWithAttributesAndMethods.method(), "You called a Method"
        )

    def test_classes_with_initializers(self):
        self.assertEqual(classes.Boy().sex, "M")
        self.assertEqual(classes.Girl(sex="F").sex, "F")
        self.assertEqual(classes.Other(sex="?").sex, "?")

    def test_me_knows_classes(self):
        self.assertEqual(classes.Me().last_name, "LastName")
        self.assertEqual(classes.SisterA().last_name, "LastName")
        self.assertEqual(classes.ChildA().last_name, "LastName")
        self.assertEqual(classes.ChildB().last_name, "LastName")
        self.assertEqual(classes.BrotherA().last_name, "LastName")
        self.assertEqual(classes.SisterB().last_name, "LastName")
        self.assertEqual(classes.BrotherA().last_name, "LastName")
        self.assertEqual(classes.SisterC().last_name, "LastName")

        self.assertEqual(classes.Me().first_name, "me")
        self.assertEqual(classes.SisterA().first_name, "sisterA")
        self.assertEqual(classes.ChildA().first_name, "ChildA")
        self.assertEqual(classes.ChildB().first_name, "ChildB")
        self.assertEqual(classes.BrotherA().first_name, "BrotherA")
        self.assertEqual(classes.SisterB().first_name, "SisterB")
        self.assertEqual(classes.BrotherB().first_name, "BrotherB")
        self.assertEqual(classes.SisterC().first_name, "SisterC")

        self.assertEqual(classes.Me().sex, "M")
        self.assertEqual(classes.SisterA().sex, "F")
        self.assertEqual(classes.ChildA().sex, "M")
        self.assertEqual(classes.ChildB().sex, "F")
        self.assertEqual(classes.BrotherA().sex, "M")
        self.assertEqual(classes.SisterB().sex, "F")
        self.assertEqual(classes.BrotherA().sex, "M")
        self.assertEqual(classes.SisterC().sex, "F")

        self.assertEqual(classes.Me().year_of_birth, 1979)
        self.assertEqual(classes.SisterA().year_of_birth, 1981)
        self.assertEqual(classes.ChildA().year_of_birth, 2010)
        self.assertEqual(classes.ChildB().year_of_birth, 2012)
        self.assertEqual(classes.BrotherA().year_of_birth, 1983)
        self.assertEqual(classes.SisterB().year_of_birth, 1985)
        self.assertEqual(classes.BrotherB().year_of_birth, 1987)
        self.assertEqual(classes.SisterC().year_of_birth, 1989)

        self.assertEqual(classes.Me().age(), datetime.datetime.now().year - 1979)
        self.assertEqual(classes.SisterA().age(), datetime.datetime.now().year - 1981)
        self.assertEqual(classes.ChildA().age(), datetime.datetime.now().year - 2010)
        self.assertEqual(classes.ChildB().age(), datetime.datetime.now().year - 2012)
        self.assertEqual(classes.BrotherA().age(), datetime.datetime.now().year - 1983)
        self.assertEqual(classes.SisterB().age(), datetime.datetime.now().year - 1985)
        self.assertEqual(classes.BrotherB().age(), datetime.datetime.now().year - 1987)
        self.assertEqual(classes.SisterC().age(), datetime.datetime.now().year - 1989)

        self.assertEqual(classes.Me().is_minor(), False)
        self.assertEqual(classes.SisterA().is_minor(), False)
        self.assertEqual(classes.ChildA().is_minor(), True)
        self.assertEqual(classes.ChildB().is_minor(), True)
        self.assertEqual(classes.BrotherA().is_minor(), False)
        self.assertEqual(classes.SisterB().is_minor(), False)
        self.assertEqual(classes.BrotherB().is_minor(), False)
        self.assertEqual(classes.SisterC().is_minor(), False)

    def test_listing_class_attributes(self):
        self.assertEqual(
            dir(classes.LastName()),
            [
                "__class__",
                "__delattr__",
                "__dict__",
                "__dir__",
                "__doc__",
                "__eq__",
                "__format__",
                "__ge__",
                "__getattribute__",
                "__gt__",
                "__hash__",
                "__init__",
                "__init_subclass__",
                "__le__",
                "__lt__",
                "__module__",
                "__ne__",
                "__new__",
                "__reduce__",
                "__reduce_ex__",
                "__repr__",
                "__setattr__",
                "__sizeof__",
                "__str__",
                "__subclasshook__",
                "__weakref__",
                "age",
                "first_name",
                "is_minor",
                "last_name",
                "sex",
                "year_of_birth",
            ],
        )


if __name__ == "__main__":
    unittest.main()
