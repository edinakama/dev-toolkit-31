import time
import functools
import random

def retry_operation(max_attempts=3, delay=1.0, backoff=2):
    """decorator for exponential backoff retries"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_attempts=3, delay=0.5)
def fetch_resource(url):
    """placeholder for network interaction"""
    import urllib.request
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status