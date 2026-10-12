import time
from typing import Any, Callable, Dict, Tuple


class AdaptiveCacheSlot:
    __slots__ = ("value", "timestamp", "hit_count", "cost")

    def __init__(self, value: Any, cost: float) -> None:
        self.value = value
        self.timestamp = time.monotonic()
        self.hit_count = 0
        self.cost = cost


class CoreOptimizer:
    """Dynamic performance optimizer utilizing cost-weighted LFU/LRU adaptive caching."""

    def __init__(self, min_cost_threshold: float = 0.0001, max_entries: int = 256) -> None:
        self.min_cost_threshold = min_cost_threshold
        self.max_entries = max_entries
        self._cache: Dict[Tuple[Any, ...], AdaptiveCacheSlot] = {}

    def memoize(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            if key in self._cache:
                slot = self._cache[key]
                slot.hit_count += 1
                return slot.value

            start_time = time.monotonic()
            result = func(*args, **kwargs)
            duration = time.monotonic() - start_time

            if duration >= self.min_cost_threshold:
                if len(self._cache) >= self.max_entries:
                    self._evict_least_valuable()
                self._cache[key] = AdaptiveCacheSlot(result, duration)

            return result

        return wrapper

    def _evict_least_valuable() -> None:
        now = time.monotonic()
        scored_keys = [
            (key, (slot.hit_count * slot.cost) / (now - slot.timestamp + 1e-5))
            for key, slot in self._cache.items()
        ]
        if scored_keys:
            worst_key = min(scored_keys, key=lambda item: item[1])[0]
            del self._cache[worst_key]

    def clear() -> None:
        self._cache.clear()


engine = CoreOptimizer()
