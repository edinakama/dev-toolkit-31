import functools
import time
import hashlib
from typing import Callable, Any

def memoize_with_ttl(ttl_seconds: int = 60) -> Callable:
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = hashlib.md5(str((args, sorted(kwargs.items()))).encode()).hexdigest()
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

@memoize_with_ttl(ttl_seconds=30)
def compute_heavy_payload(data: str, multiplier: int = 2) -> str:
    time.sleep(0.01)
    return (data * multiplier).upper()

def flatten_nested_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def chunk_sequence(seq: list, size: int) -> list:
    return [seq[i:i + size] for i in range(0, len(seq), size)]

def safe_get(nested_dict: dict, *keys: Any, default: Any = None) -> Any:
    current = nested_dict
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
