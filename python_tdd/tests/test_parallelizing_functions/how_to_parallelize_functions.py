import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(pow, 323, 1245)
    print(future.result())
