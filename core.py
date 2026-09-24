import functools
import time
from typing import Callable, Any, Dict, Tuple


class AdaptiveCache:
    """Dynamic self-tuning memoization cache with execution timing feedback."""

    def __init__(self, target_latency_ms: float = 50.0, max_size: int = 1024):
        self.target_latency = target_latency_ms / 1000.0
        self.max_size = max_size
        self._store: Dict[Tuple[Any, ...], Tuple[Any, float, float]] = {}
        self._hits = 0
        self._misses = 0

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            if key in self._store:
                val, _, expire_time = self._store[key]
                if now < expire_time:
                    self._hits += 1
                    return val

            self._misses += 1
            start_time = time.monotonic()
            result = func(*args, **kwargs)
            duration = time.monotonic() - start_time

            ttl = max(0.5, duration * 20.0)
            if len(self._store) >= self.max_size:
                self._evict_stale(now)

            self._store[key] = (result, duration, now + ttl)
            return result

        return wrapper

    def _evict_stale(self, current_time: float) -> None:
        expired = [k for k, v in self._store.items() if current_time >= v[2]]
        for k in expired:
            del self._store[k]

        if len(self._store) >= self.max_size:
            sorted_keys = sorted(self._store.keys(), key=lambda k: self._store[k][1])
            for k in sorted_keys[: self.max_size // 4]:
                del self._store[k]

    def stats(self) -> Dict[str, Any]:
        total = self._hits + self._misses
        hit_rate = (self._hits / total) if total > 0 else 0.0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 4),
            "cached_items": len(self._store),
        }


def memoize_adaptive(target_latency_ms: float = 50.0):
    return AdaptiveCache(target_latency_ms=target_latency_ms)
