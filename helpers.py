import time
import functools
import itertools
from typing import Callable, Any, Iterable, List

def retry(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def chunker(iterable: Iterable, size: int) -> Iterable[List[Any]]:
    iterator = iter(iterable)
    while True:
        chunk = list(itertools.islice(iterator, size))
        if not chunk:
            break
        yield chunk

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def memoize_transient(ttl_seconds: int = 60):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                val, ts = cache[args]
                if now - ts < ttl_seconds:
                    return val
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator