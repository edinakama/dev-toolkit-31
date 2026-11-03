import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-31')

class ToolkitError(Exception):
    """Base exception for the toolkit."""
    pass

class EdgeCaseRegistry:
    def __init__(self):
        self.handlers = {}

    def register(self, exception_type: type):
        def decorator(func: Callable):
            self.handlers[exception_type] = func
            return func
        return decorator

registry = EdgeCaseRegistry()

def resilient_wrapper(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler = registry.handlers.get(type(e))
            if handler:
                return handler(e)
            logger.error(f"Unhandled edge case in {func.__name__}: {e}")
            raise ToolkitError(f"Critical failure: {e}") from e
    return wrapper

@registry.register(ZeroDivisionError)
def handle_zero(e: Exception) -> float:
    return float('inf')

@registry.register(KeyError)
def handle_missing_key(e: Exception) -> None:
    return None