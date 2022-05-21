def contradiction(a, b):
    return False


def converse_implication(a, b):
    return a or not b


def converse_nonimplication(a, b):
    return not a and b


def exclusive_disjunction(a, b):
    return (a and not b) or (not a and b)


def logical_conjunction(a, b):
    return a and b


def logical_disjunction(a, b):
    return a or b


def logical_equality(a, b):
    return not (a or b) or (a and b)


def logical_implication(a, b):
    return not a or b

def logical_nand(a, b):
    return not (a and b)

def logical_nor(a, b):
    return not (a or b)

def material_nonimplication(a, b):
    return a and not b

def negate_first(a, b):
    return not a

def negate_second(a, b):
    return not b

def project_first(a, b):
    return a

def project_second(a, b):
    return b

def logical_negation(a):
    return not a

def tautology(*args):
    return True

def logical_false(*args):
    return False

def logical_true(*args):
    return True

def logical_identity(a):
    return a