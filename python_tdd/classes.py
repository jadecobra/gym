import datetime


class ClassWithObject(object):
    pass


class ClassWithParentheses(object):
    pass


class ClassWithPass(object):
    pass


class ClassWithAttributes(object):
    attribute_a = "AttributeA"
    attribute_b = "AttributeB"
    attribute_c = "AttributeC"
    attribute_d = "AttributeD"


class ClassWithMethods(object):
    def method_a():
        return "You called MethodA"

    def method_b():
        return "You called MethodB"

    def method_c():
        return "You called MethodC"

    def method_d():
        return "You called MethodD"


class ClassWithAttributesAndMethods(object):

    attribute = "Attribute"

    def method():
        return "You called a Method"


class Boy(object):
    def __init__(self, sex="M"):
        self.sex = sex


class Girl(Boy):
    pass


class Other(Girl):
    pass


class LastName(object):
    def __init__(
        self, first_name=None, last_name="LastName", sex="M", year_of_birth=None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.year_of_birth = year_of_birth

    def age(self):
        return datetime.datetime.now().year - self.year_of_birth

    def is_minor(self):
        return self.age() < 21


class Me(LastName):
    def __init__(self):
        super().__init__(first_name="me", year_of_birth=1979)


class SisterA(LastName):
    def __init__(self):
        super().__init__(first_name="sisterA", sex="F", year_of_birth=1981)


class ChildA(LastName):
    def __init__(self):
        super().__init__(first_name="ChildA", year_of_birth=2010)


class ChildB(LastName):
    def __init__(self):
        super().__init__(first_name="ChildB", sex="F", year_of_birth=2012)


class BrotherA(LastName):
    def __init__(self):
        super().__init__(first_name="BrotherA", year_of_birth=1983)


class SisterB(LastName):
    def __init__(self):
        super().__init__(first_name="SisterB", sex="F", year_of_birth=1985)


class SisterC(LastName):
    def __init__(self):
        super().__init__(first_name="SisterC", sex="F", year_of_birth=1989)


class BrotherB(LastName):
    def __init__(self):
        super().__init__(first_name="BrotherB", year_of_birth=1987)
