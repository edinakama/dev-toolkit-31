import time
import functools
import random
import logging

logger = logging.getLogger('dev-toolkit-31')

class TransientNetworkError(Exception):
    pass

def retry_with_jitter(max_retries=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (TransientNetworkError, ConnectionError) as e:
                    attempts += 1
                    if attempts >= max_retries:
                        logger.error(f'failed after {attempts} attempts')
                        raise
                    sleep_time = (base_delay * (2 ** attempts)) + (random.random() * 0.5)
                    logger.warning(f'retry {attempts}/{max_retries} after {sleep_time:.2f}s')
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold=3):
        self.failures = 0
        self.threshold = failure_threshold

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.failures >= self.threshold:
                raise RuntimeError('circuit is currently open')
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                raise e
        return wrapper