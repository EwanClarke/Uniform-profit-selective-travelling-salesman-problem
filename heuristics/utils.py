from time import perf_counter

def runtime_counter(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        func(args, kwargs)
        time_elapsed = perf_counter() - start
        print(f"time elapsed: {time_elapsed}")
    return wrapper

def swap_edges(path, i, j):
    i += 1
    while i < j:
        temp = path[i]
        path[i] = path[j]
        path[j] = temp
        i += 1
        j -= 1

def path_length(path):
    if len(path) <= 1:
        return 0
    nodes = len(path)
    length = path[-1].calculate_distance(path[0])
    for i in range(0, nodes-1):
        length += path[i].calculate_distance(path[i+1])
    return length