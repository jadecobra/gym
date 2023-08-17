import operator

def count(start=0, step=1):
    # count(10) --> 10 11 12 13 14 ...
    # count(2.5, 0.5) --> 2.5 3.0 3.5 4.0 ...
    # how to create consecutive datapoints
    while True:
        yield start
        start += step

def cycle(iterable):
    # return elements from iterable and save a copy
    # cycle('ABCD') --> A B C D A B C D ...
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        for element in saved:
            yield element

def repeat(object, times=None):
    # repeat(10, 4) --> 10 10 10 10
    if times is None:
        while True:
            yield object
    else:
        for i in range(times):
            yield object

def accumulate_results_of_binary_functions(iterable, function=operator.add, *, initial=None):
    'Return running totals'
    # accumulate_results_of_binary_functions([1, 2, 3, 4, 5]) --> 1 3 6 10 15
    # accumulate_results_of_binary_functions([1, 2, 3, 4, 5], initial=100) --> 100 101 103 106 110 115
    # accumulate_results_of_binary_functions([1, 2, 3, 4, 5], operator.mul) --> 1 2 6 24 120
    iterable_object = iter(iterable)
    total = initial
    if initial is None:
        try:
            total = next(iterable_object)
        except StopIteration:
            return
    yield total
    for element in iterable_object:
        total = function(total, element)
        yield total

def chain(*iterables):
    # chain('ABC', 'DEF') --> A B C D E F
    for iterable in iterables:
        for element in iterable:
            yield element

def compress(data, selectors):
    # compress('ABCDEF', [1, 0, 1, 0, 1, 1]) --> A C E F
    return (key for key, value in zip(data, selectors) if value)


def drop_while_predicate_true(predicate, iterable):
    # drop_while(lambda x: x<5, [1, 4, 6, 4, 1]) --> 6 4 1
    iterable = iter(iterable)
    for element in iterable:
        if not predicate(element):
            yield element
            break
    for element in iterable:
        yield element

def filter_false(predicate, iterable):
    # filter_false(lambda x: x%2==0, range(10)) --> 0 2 4 6 8
    if predicate is None:
        predicate = bool
    for x in iterable:
        if not predicate(x):
            yield x

class groupby:
    # [key for key, group in groupby('AAAABBBCCD')] --> A B C D
    # [list(g) for k, g in groupby('AAAABBBCCD')] --> AAAA BBB CC D

    def __init__(self, iterable, key=None):
        if key is None:
            key = lambda x: x
        self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()

    def __iter__(self):
        return self

    def __next__(self):
        self.id = object()
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)
            self.currkey = self.keyfunc(self.currvalue)
        self.tgtkey = self.currkey
        return (self.currkey, self._grouper(self.tgtkey, self.id))

    def _grouper(self, tgtkey, id):
        while self.id is id and self.currkey == tgtkey:
            yield self.currvalue
            try:
                self.currvalue = next(self.it)
            except StopIteration:
                return
            self.currkey = self.keyfunc(self.currvalue)