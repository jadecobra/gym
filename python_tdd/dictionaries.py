import datetime

def a_dict():
    return {"key": "value"}


def another_dict():
    return {"key": "value"}


def person():
    return {
        "first_name": "me",
        "last_name": "last_name",
        "year_of_birth": "1986",
        "sex": "M",
        "age": "34",
    }


def person_factory(first_name=None, last_name="last_name", year_of_birth=None, sex="F"):
    return dict(
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        year_of_birth=year_of_birth,
        age=datetime.datetime.now().year - year_of_birth,
    )
