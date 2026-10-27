import functools
import logging
from typing import Callable, Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dev-toolkit-31')

class Registry:
    _storage: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(func: Callable):
            cls._storage[key] = func
            return func
        return decorator

    @classmethod
    def execute(cls, key: str, *args, **kwargs):
        if key not in cls._storage:
            raise KeyError(f'no operation found for {key}')
        return cls._storage[key](*args, **kwargs)

def resilient(retries: int = 3):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    logger.warning(f'attempt {attempt+1} failed: {e}')
            raise last_ex
        return wrapper
    return decorator

@Registry.register('noop')
def noop(*args, **kwargs):
    return None

def clean_dict(data: Dict) -> Dict:
    return {k: v for k, v in data.items() if v is not None}