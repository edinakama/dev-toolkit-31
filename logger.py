import sys
import datetime
from functools import wraps

class DevLogger:
    def __init__(self, prefix: str = "[dev-toolkit-31]"):
        self.prefix = prefix

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = f"{timestamp} {self.prefix} {level}: {message}"
        print(output, file=sys.stderr if level == "ERROR" else sys.stdout)

    def trace(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.log(f"executing {func.__name__} with {args} {kwargs}")
            result = func(*args, **kwargs)
            self.log(f"{func.__name__} returned {result}")
            return result
        return wrapper

def get_logger(name: str = "default"):
    return DevLogger(f"[{name}]")

def silent_failure(fallback=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return fallback
        return wrapper
    return decorator