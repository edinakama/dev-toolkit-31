import functools
import time
import uuid
from typing import Callable, Any

def memoize_with_ttl(seconds: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache and now - cache[key]['ts'] < seconds:
                return cache[key]['val']
            result = func(*args, **kwargs)
            cache[key] = {'val': result, 'ts': now}
            return result
        return wrapper
    return decorator

def generate_id(prefix: str = 'dev') -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

def flatten(nested: list) -> list:
    return [item for sublist in nested for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]

def retry(attempts: int = 3, delay: float = 0.1) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator