import functools
import time
from typing import Callable, Any, Dict

CACHE_STORE: Dict[str, Any] = {}

class memoize_with_ttl:
    def __init__(self, ttl: int = 300):
        self.ttl = ttl

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{hash(args)}:{hash(frozenset(kwargs.items()))}"
            now = time.time()
            if key in CACHE_STORE:
                val, expiry = CACHE_STORE[key]
                if now < expiry:
                    return val
            result = func(*args, **kwargs)
            CACHE_STORE[key] = (result, now + self.ttl)
            return result
        return wrapper

@memoize_with_ttl(ttl=60)
def compute_heavy_data(n: int) -> int:
    result = 0
    for i in range(n):
        result += i**2
    return result

def batch_process(data: list) -> list:
    # Using list comprehension for speed optimization
    return [compute_heavy_data(x) for x in data]

if __name__ == '__main__':
    print(batch_process([1000, 2000, 1000]))