import time
import functools
import random

def exponential_backoff(max_retries=3, base_delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkHandler:
    def __init__(self):
        self.history = []

    @exponential_backoff(max_retries=4, base_delay=1.0)
    def fetch_resource(self, url):
        # Simulate unstable network condition
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach {url}")
        return f"Data from {url}"

def process_network_queue(urls):
    handler = NetworkHandler()
    results = {}
    for url in urls:
        try:
            results[url] = handler.fetch_resource(url)
        except Exception:
            results[url] = None
    return results