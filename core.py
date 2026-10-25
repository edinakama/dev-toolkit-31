import functools
import time
import collections

class memoize_with_ttl:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}
        self.expiry = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache and now < self.expiry[key]:
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.expiry[key] = now + self.ttl
            return result
        return wrapper

class CoreProcessor:
    def __init__(self):
        self.registry = collections.deque(maxlen=1000)

    @memoize_with_ttl(ttl=30)
    def heavy_computation(self, data: int) -> int:
        return sum(i * i for i in range(data))

    def process_batch(self, items):
        return [self.heavy_computation(i) for i in items]

if __name__ == '__main__':
    cp = CoreProcessor()
    print(cp.process_batch([1000, 2000, 1000]))