import json
import time
import functools
from typing import Callable, Any

def retry_on_failure(max_retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1: raise e
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

def deep_freeze(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def time_execution(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'[dev-toolkit-31] {func.__name__} took {elapsed:.4f}s')
        return result
    return wrapper

def chunk_list(data: list, size: int):
    return [data[i:i + size] for i in range(0, len(data), size)]

class AttributeDict(dict):
    def __getattr__(self, key):
        return self[key] if key in self else None
    def __setattr__(self, key, value):
        self[key] = value