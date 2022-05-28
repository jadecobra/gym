def model(expectations=None, reality=None):
    while reality < expectations:
        reality += expectations - reality
    return reality + 1


def model(*args):
    return 2
