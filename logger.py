import time
import collections
import functools

class BatchLogger:
    def __init__(self, interval=5.0, capacity=100):
        self.interval = interval
        self.capacity = capacity
        self.buffer = collections.deque()
        self.last_flush = time.monotonic()

    def log(self, message):
        self.buffer.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")
        if len(self.buffer) >= self.capacity or (time.monotonic() - self.last_flush) > self.interval:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
        chunk = list(self.buffer)
        self.buffer.clear()
        self.last_flush = time.monotonic()
        print('\n'.join(chunk))

def optimized_logger(func):
    logger = BatchLogger()
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.log(f"{func.__name__} executed in {elapsed:.6f}s")
        return result
    return wrapper