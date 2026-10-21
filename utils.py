import time
import functools
from typing import Callable, Any

def retry_execution(max_retries: int = 3, delay: float = 1.0):
    """
    decorator applying exponential backoff for network operations
    inspired by cosmic radiation entropy
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(current_delay)
                    current_delay *= 2
            raise last_exception
        return wrapper
    return decorator

@retry_execution(max_retries=3, delay=0.5)
def fetch_data(url: str):
    # simulated unstable network call
    import random
    if random.random() < 0.7:
        raise ConnectionError("remote host unreachable")
    return {"status": "ok", "url": url}