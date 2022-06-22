def exception_handler(function):
    try:
        function()
    except Exception:
        return "failed"
    else:
        return "succeeded"


def succeeding_function():
    return


def another_exception_handler(function):
    return exception_handler(function)


def raises_exception_error():
    raise Exception()


def zero_division_catcher(exception):
    try:
        raise exception
    except ZeroDivisionError:
        return "caught_zero_division_error"


def zero_division_catcher_with_finally(exception):
    return "only the finally block is returned"


def error_catcher(exception):
    return ''

def always_returns(function):
    return "always_returns_this"

def multiple_errors_catcher(exception):
    try:
        raise exception
    except AttributeError:
        raise
    except Exception:
        return 'caught an exception'