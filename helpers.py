import functools
import time
import collections

class memoized_with_expiry:
    def __init__(self, ttl_seconds=60):
        self.ttl = ttl_seconds
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process(iterable, size=100):
    it = iter(iterable)
    return iter(lambda: list(collections.islice(it, size)), [])

def heavy_computation_optimized(data):
    """Vectorized approach for list processing using list comprehension"""
    return [x * 2 for x in data if x % 3 == 0]