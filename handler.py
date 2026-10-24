import functools
import time
import collections
from typing import Callable, Any, Dict

def memoize_with_expiry(ttl: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        cache: Dict[tuple, tuple] = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def deep_flatten(items: list) -> list:
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(deep_flatten(item))
        else:
            result.append(item)
    return result

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def pluck(data: list[dict], key: str) -> list:
    return [d[key] for d in data if key in d]

class Registry:
    def __init__(self):
        self._store = collections.defaultdict(list)
    
    def register(self, tag: str):
        def decorator(func: Callable):
            self._store[tag].append(func)
            return func
        return decorator

    def execute(self, tag: str, *args, **kwargs):
        return [f(*args, **kwargs) for f in self._store.get(tag, [])]