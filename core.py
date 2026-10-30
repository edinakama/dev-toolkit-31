import functools
import time
import uuid
from typing import Callable, Any

def memoize_with_expiry(ttl: int = 60):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache and now - cache[key]['ts'] < ttl:
                return cache[key]['val']
            result = func(*args, **kwargs)
            cache[key] = {'val': result, 'ts': now}
            return result
        return wrapper
    return decorator

def generate_slug(prefix: str = 'dev') -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def batch_process(items: list, size: int):
    return [items[i:i + size] for i in range(0, len(items), size)]

def retry_operation(attempts: int = 3, delay: float = 1.0):
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