import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    # Exponential backoff with jitter to prevent thundering herd
                    sleep_time = delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold: int = 5):
        self.failures = 0
        self.threshold = failure_threshold
        self.is_open = False

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.is_open:
                raise ConnectionError("Circuit is currently open. Request rejected.")
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                if self.failures >= self.threshold:
                    self.is_open = True
                raise e
        return wrapper