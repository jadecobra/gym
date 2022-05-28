import time
import concurrent.futures

def wait_five_minutes(message, index):
    time.sleep(5)
    print(message)
    return index
def wait_on_b():
    # B will never complete because it is waiting on A
    return wait_five_minutes(B.result(), 5)

def wait_on_a():
    # A will never complete because it is waiting on B
    return wait_five_minutes(A.result(), 6)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
A = executor.submit(wait_on_b)
B = executor.submit(wait_on_a)
