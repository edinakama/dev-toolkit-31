import functools
import time
import json
from pathlib import Path
from typing import Callable, Any

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'[dev-toolkit-31] {func.__name__} took {time.perf_counter() - start:.4f}s')
        return result
    return wrapper

def load_json_magic(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def memoize_file(filepath: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        cache = load_json_magic(filepath)
        @functools.wraps(func)
        def wrapper(*args: Any) -> Any:
            key = str(args)
            if key not in cache:
                cache[key] = func(*args)
                Path(filepath).write_text(json.dumps(cache))
            return cache[key]
        return wrapper
    return decorator

def retry_softly(attempts: int = 3, delay: float = 0.1):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay * (i + 1))
            raise last_err
        return wrapper
    return decorator