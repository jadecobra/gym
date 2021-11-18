import unittest

from classes import (
    ClassWithPass, ClassWithParentheses, ClassWithObject, ClassWithAttributes, ClassWithMethods, ClassWithAttributesAndMethods, Me, SisterA, ChildA, ChildB, BrotherA, SisterB, BrotherB, SisterC, LastName, Boy, Girl, Other
)


class TestClasses(unittest.TestCase):

	def test_class_definitions_with_pass(self):
		self.assertIsInstance(ClassWithPass(), object)

	def test_class_definitions_with_parentheses(self):
		self.assertIsInstance(ClassWithParentheses(), object)

	def test_class_definition_with_object(self):
		self.assertIsInstance(ClassWithObject(), object)

	def test_classes_with_attributes(self):
		self.assertEqual(
			ClassWithAttributes.attribute_a, 'AttributeA'
		)
		self.assertEqual(
			ClassWithAttributes.attribute_b, 'AttributeB'
		)
		self.assertEqual(
			ClassWithAttributes.attribute_c, 'AttributeC'
		)
		self.assertEqual(
			ClassWithAttributes.attribute_d, 'AttributeD'
		)

	def test_classes_with_methods(self):
		self.assertEqual(
			ClassWithMethods.method_a(), 'MethodA'
		)
		self.assertEqual(
			ClassWithMethods.method_b(), 'MethodB'
		)
		self.assertEqual(
			ClassWithMethods.method_c(), 'MethodC'
		)
		self.assertEqual(
			ClassWithMethods.method_d(), 'MethodD'
		)

	def test_classes_with_attributes_and_methods(self):
		self.assertEqual(
			ClassWithAttributesAndMethods.attribute,
			'Attribute'
		)
		self.assertEqual(
			ClassWithAttributesAndMethods.method(), 'Method'
		)

	def test_classes_with_initializers(self):
		self.assertEqual(Boy().sex, 'M')
		self.assertEqual(Girl(sex='F').sex, 'F')
		self.assertEqual(Other(sex='?').sex, '?')

	def test_me_knows_classes(self):
		self.assertEqual(Me().last_name, 'LastName')
		self.assertEqual(SisterA().last_name, 'LastName')
		self.assertEqual(ChildA().last_name, 'LastName')
		self.assertEqual(ChildB().last_name, 'LastName')
		self.assertEqual(BrotherA().last_name, 'LastName')
		self.assertEqual(SisterB().last_name, 'LastName')
		self.assertEqual(BrotherA().last_name, 'LastName')
		self.assertEqual(SisterC().last_name, 'LastName')

		self.assertEqual(Me().first_name, 'me')
		self.assertEqual(SisterA().first_name, 'sisterA')
		self.assertEqual(ChildA().first_name, 'ChildA')
		self.assertEqual(ChildB().first_name, 'ChildB')
		self.assertEqual(BrotherA().first_name, 'BrotherA')
		self.assertEqual(SisterB().first_name, 'SisterB')
		self.assertEqual(BrotherA().first_name, 'BrotherB')
		self.assertEqual(SisterC().first_name, 'SisterC')

		self.assertEqual(Me().sex, 'M')
		self.assertEqual(SisterA().sex, 'F')
		self.assertEqual(ChildA().sex, 'M')
		self.assertEqual(ChildB().sex, 'F')
		self.assertEqual(BrotherA().sex, 'M')
		self.assertEqual(SisterB().sex, 'F')
		self.assertEqual(BrotherA().sex, 'M')
		self.assertEqual(SisterC().sex, 'F')

		self.assertEqual(Me().year_of_birth, 1986)
		self.assertEqual(SisterA().year_of_birth, 1983)
		self.assertEqual(ChildA().year_of_birth, 2014)
		self.assertEqual(ChildB().year_of_birth, 2017)
		self.assertEqual(BrotherA().year_of_birth, 1978)
		self.assertEqual(SisterB().year_of_birth, 1980)
		self.assertEqual(BrotherB().year_of_birth, 1983)
		self.assertEqual(SisterC().year_of_birth, 1990)

		self.assertEqual(Me().age(), 35)
		self.assertEqual(SisterA().age(), 38)
		self.assertEqual(ChildA().age(), 7)
		self.assertEqual(ChildB().age(), 4)
		self.assertEqual(BrotherA().age(), 43)
		self.assertEqual(SisterB().age(), 41)
		self.assertEqual(BrotherB().age(), 38)
		self.assertEqual(SisterC().age(), 31)

		self.assertEqual(Me().is_minor(), False)
		self.assertEqual(SisterA().is_minor(), False)
		self.assertEqual(ChildA().is_minor(), True)
		self.assertEqual(ChildB().is_minor(), True)
		self.assertEqual(BrotherA().is_minor(), False)
		self.assertEqual(SisterB().is_minor(), False)
		self.assertEqual(BrotherB().is_minor(), False)
		self.assertEqual(SisterC().is_minor(), False)

	@unittest.skip
	def test_listing_class_attributes(self):
		self.assertEqual(
			dir(LastName),
			[
				'__class__',
				'__delattr__',
				'__dict__',
				'__dir__',
				'__doc__',
				'__eq__',
				'__format__',
				'__ge__',
				'__getattribute__',
				'__gt__',
				'__hash__',
				'__init__',
				'__init_subclass__',
				'__le__',
				'__lt__',
				'__module__',
				'__ne__',
				'__new__',
				'__reduce__',
				'__reduce_ex__',
				'__repr__',
				'__setattr__',
				'__sizeof__',
				'__str__',
				'__subclasshook__',
				'__weakref__',
				'age',
				'is_minor',
				'last_name',
				'sex'
			]
		)
