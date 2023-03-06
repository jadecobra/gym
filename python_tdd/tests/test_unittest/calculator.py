def add(x, y):
    return x + y

def subtract(x, y):
    return 0

def divide(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return 'You tried it'

def multiply(x, y):
    return x * y