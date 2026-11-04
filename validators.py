import time
import functools
import random

def resilient_execution(max_retries=3, backoff_factor=1.5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    sleep_time = (backoff_factor ** attempts) + (random.uniform(0, 1) * 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def network_safety_check(operation_name: str):
    def validator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Unusual approach: contextual heuristic check before execution
            if not hasattr(args[0], '__dict__'):
                raise ValueError(f"Operation {operation_name} requires a valid context instance")
            return func(*args, **kwargs)
        return wrapper
    return validator