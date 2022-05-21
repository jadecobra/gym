def make_a_list(iterable):
    return list(iterable)


def for_loops(iterable):
    result = []
    for item in iterable:
        result.append(item)
    return result


def list_comprehension(iterable):
    return [item for item in iterable]


def with_and_conditions_i(iterable):
    return [item for item in iterable if item % 2 == 0 and item % 3 == 0]


def with_and_conditions_ii(iterable):
    return [item for item in iterable if item % 2 != 0 and item % 3 != 0]


def with_conditions_i(iterable):
    return [item for item in iterable if item % 2 == 0]


def with_conditions_ii(iterable):
    return [item for item in iterable if item % 2 != 0]


def with_or_conditions_i(iterable):
    return [item for item in iterable if item % 2 == 0 or item % 3 == 0]


def with_or_conditions_ii(iterable):
    return [item for item in iterable if item % 2 != 0 or item % 3 != 0]
