import sys
import time
import inspect
from datetime import datetime

def log_dispatch(level, message):
    caller = inspect.stack()[2]
    context = f"{caller.filename.split('/')[-1]}:{caller.lineno}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = f"[{timestamp}] [{level.upper()}] ({context}) -> {message}"
    sys.stdout.write(f"{output}\n")
    sys.stdout.flush()

class CreativeLogger:
    def __init__(self, prefix="dev-toolkit-31"):
        self.prefix = prefix

    def info(self, msg):
        log_dispatch("info", f"{self.prefix} | {msg}")

    def warn(self, msg):
        log_dispatch("warn", f"{self.prefix} | !!! {msg} !!!")

    def error(self, msg):
        log_dispatch("crit", f"{self.prefix} | >>> {msg.upper()} <<<")

    def stopwatch(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            log_dispatch("perf", f"function {func.__name__} took {elapsed:.4f}s")
            return result
        return wrapper