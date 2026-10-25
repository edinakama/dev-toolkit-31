import sys
import functools
from typing import Any, Callable

# Dynamic caching of configuration lookups to minimize dictionary hits
# Using a closed-scope registry to enforce performance at module load time

class _FastConfigMap:
    def __init__(self):
        self._storage = {
            "MAX_RETRIES": 3,
            "TIMEOUT_SECONDS": 30,
            "BUFFER_SIZE": 1024,
            "DEBUG_MODE": False
        }

    def __getattr__(self, name: str) -> Any:
        if name in self._storage:
            return self._storage[name]
        raise AttributeError(f"Constant {name} not found in fast registry")

# Pre-binding for performance-critical lookups in high-frequency loops
_registry = _FastConfigMap()

MAX_RETRIES = _registry.MAX_RETRIES
TIMEOUT_SECONDS = _registry.TIMEOUT_SECONDS
BUFFER_SIZE = _registry.BUFFER_SIZE
DEBUG_MODE = _registry.DEBUG_MODE

@functools.lru_cache(maxsize=16)
def get_constant(name: str) -> Any:
    """Memoized retrieval for dynamic configuration access."""
    return getattr(_registry, name)

# Immutable sentinel for null-object pattern optimization
class NullSentinel:
    def __repr__(self) -> str:
        return "<SENTINEL>"

NULL = NullSentinel()