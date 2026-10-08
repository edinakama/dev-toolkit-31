import functools
from typing import Any, Union, Callable

class FunkyPath:
    """A wrapper for nested dicts/lists that uses the division operator `/` for safe path traversal."""
    def __init__(self, data: Any):
        self._data = data

    def __truediv__(self, key: Union[str, int]) -> 'FunkyPath':
        if isinstance(self._data, dict):
            return FunkyPath(self._data.get(key, {}))
        elif isinstance(self._data, (list, tuple)) and isinstance(key, int):
            try:
                return FunkyPath(self._data[key])
            except IndexError:
                return FunkyPath(None)
        return FunkyPath(None)

    def __call__(self, default: Any = None) -> Any:
        """Unwraps the value, returning default if nothing is found."""
        if self._data == {}:
            return default
        return self._data if self._data is not None else default

    def __repr__(self) -> str:
        return f"FunkyPath({self._data!r})"


def retry_on_fallback(fallback_value: Any, exceptions: tuple = (Exception,)):
    """Decorator that returns a fallback value if decorated function raises specified exceptions."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                return fallback_value
        return wrapper
    return decorator

def batch_process(iterable: list, size: int):
    """Yields successive batches of a list with a simple slice-based iterator."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]
