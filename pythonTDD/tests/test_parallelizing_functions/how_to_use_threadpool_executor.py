import concurrent.futures


def an_iterable():
    return ['A', 'B', 'C', 'D']

def function(kwarg1=None, kwarg2=None):
    return {kwarg1: kwarg2.lower()}

def display_results(executions):
    for execution in concurrent.futures.as_completed(executions):
        try:
            print(f'{executions[execution]} returned {execution.result()}')
        except Exception as error:
            print(f'{executions[execution]} generated an exception: {error}')

def parallelize(function, iterable, max_workers=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        display_results({
            executor.submit(
                function,
                kwarg1=f'test{item}',
                kwarg2=item
            ): f'process_{index}'
            for index, item in enumerate(iterable)
        })

parallelize(
    function=function,
    iterable=an_iterable(),
)