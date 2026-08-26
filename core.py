import functools
import time

class MemoizedCore:
    def __init__(self, capacity: int = 128):
        self.capacity = capacity
        self._cache = {}
        self._order = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in self._cache:
                self._order.remove(key)
                self._order.append(key)
                return self._cache[key]
            
            result = func(*args, **kwargs)
            if len(self._cache) >= self.capacity:
                oldest = self._order.pop(0)
                del self._cache[oldest]
            
            self._cache[key] = result
            self._order.append(key)
            return result
        return wrapper

@MemoizedCore(capacity=256)
def compute_heavy_payload(data_id: int, multiplier: float = 1.0) -> float:
    time.sleep(0.001)
    return (data_id * 3.14159) ** 0.5 * multiplier

def batch_process(items: list[int]) -> list[float]:
    return [compute_heavy_payload(item) for item in items]
