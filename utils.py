import functools
import time
import threading

class memoize_with_ttl:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}
        self.lock = threading.Lock()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            with self.lock:
                if key in self.cache:
                    result, expiry = self.cache[key]
                    if now < expiry:
                        return result
                
                result = func(*args, **kwargs)
                self.cache[key] = (result, now + self.ttl)
                return result
        return wrapper

def batch_process(items, chunk_size=10):
    """Generator for memory-efficient batch iteration."""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def throttle(rate_limit=1.0):
    """Dynamic delay injection for rate-limited execution."""
    def decorator(func):
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.monotonic() - last_called[0]
            if elapsed < rate_limit:
                time.sleep(rate_limit - elapsed)
            last_called[0] = time.monotonic()
            return func(*args, **kwargs)
        return wrapper
    return decorator