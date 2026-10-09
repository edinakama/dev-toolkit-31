import json
import time
from typing import Any, Callable, Dict

def retry_execution(retries: int = 3, delay: float = 0.5) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def safe_json_load(data: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
    try:
        return json.loads(data)
    except (ValueError, TypeError):
        return default or {}

def deep_flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(deep_flatten(item))
        else:
            result.append(item)
    return result

def time_execution(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"execution took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper