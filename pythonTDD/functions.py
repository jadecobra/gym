def passthrough_with_keywords(first_name=None, last_name=None):
    return first_name, last_name


def function_with_pass():
    return


def passthrough_with_positions(first_name, last_name):
    return first_name, last_name


def function_with_return():
    return function_with_pass()


def function_with_return_none():
    return function_with_return()


def keyword_counter(**kwargs):
    return len(kwargs)


def parameter_counter(*args):
    return len(args)


def argument_counter(*args, **kwargs):
    return parameter_counter(*args) + keyword_counter(**kwargs)


def passthrough(x):
    return x


def name():
    return "my_first_name"


def joe(*args):
    return "joe"
