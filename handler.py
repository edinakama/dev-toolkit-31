import functools
import time
import logging

logging.basicConfig(level=logging.INFO)

def retry_operation(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def batch_process(iterable, chunk_size=10):
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]

def sanitize_dict(d, keys_to_strip=None):
    keys_to_strip = keys_to_strip or set()
    return {k: v for k, v in d.items() if k not in keys_to_strip}

class ExecutionContext:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        logging.info(f'Starting operation: {self.name}')
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        logging.info(f'Finished {self.name} in {elapsed:.4f}s')
        return False