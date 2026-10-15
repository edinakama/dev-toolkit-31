import time
import functools
import random
from typing import Callable, Any

def exponential_retry(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkException(Exception):
    pass

def execute_with_fallback(func: Callable, fallback_val: Any) -> Any:
    try:
        return func()
    except Exception:
        return fallback_val