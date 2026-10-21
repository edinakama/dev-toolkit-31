import functools
import threading
import collections

class ConfigCache:
    """Thread-safe memoization layer for config lookups."""
    def __init__(self, maxsize=128):
        self._cache = collections.OrderedDict()
        self._lock = threading.Lock()
        self._maxsize = maxsize

    def get(self, key, provider_func):
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                return self._cache[key]
            
            value = provider_func(key)
            self._cache[key] = value
            if len(self._cache) > self._maxsize:
                self._cache.popitem(last=False)
            return value

    def invalidate(self, key=None):
        with self._lock:
            if key: self._cache.pop(key, None)
            else: self._cache.clear()

config_store = ConfigCache()

def optimized_config_lookup(func):
    """Decorator for high-frequency configuration retrieval."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = f"{func.__name__}:{args}:{tuple(sorted(kwargs.items()))}"
        return config_store.get(key, lambda k: func(*args, **kwargs))
    return wrapper

@optimized_config_lookup
def fetch_setting(name, default=None):
    # Simulated I/O bound configuration retrieval
    return {"timeout": 30, "retry": 3}.get(name, default)