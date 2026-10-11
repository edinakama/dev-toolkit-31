import functools
import logging
import time
from typing import Callable, Any, Dict

logger = logging.getLogger('dev-toolkit-31')

class ResourceRegistry:
    def __init__(self):
        self._registry: Dict[str, Any] = {}

    def register(self, name: str, resource: Any) -> None:
        self._registry[name] = resource

    def get(self, name: str) -> Any:
        return self._registry.get(name)

def memoize_with_expiry(ttl: int = 300):
    def decorator(func: Callable):
        cache = {}
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

def batch_process(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]

def safe_execute(func: Callable, default: Any = None, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f'execution failure in {func.__name__}: {e}')
        return default