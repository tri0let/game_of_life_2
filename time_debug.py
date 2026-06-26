import time
import functools

TIMING = True

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        if TIMING:
            tic = time.perf_counter()
            value = func(*args, **kwargs)
            toc = time.perf_counter()
            elapsed_time = toc - tic
            print(f'Elapsed time: {elapsed_time:0.4f} seconds for {func}')
            return value
        else:
            return func(*args, **kwargs)
    return wrapper_timer