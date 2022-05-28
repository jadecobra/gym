class Node:

    def __init__(self, label, value):
        self.label = label
        self.value = tuple(value)

    def __repr__(self):
        return f'Node({self.label!r}, {self.value!r})'

    def sorts_before(self):
        if len(self.value) >= len(other.value):
            return False
        return other.value[: len(self.value)] == self.value