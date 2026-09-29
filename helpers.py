import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-31')

class RecoveryContext:
    def __init__(self, fallback: Any = None):
        self.fallback = fallback

def resilient_wrapper(fallback: Any = None):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, AttributeError) as e:
                logger.warning(f"silent recovery triggered for {func.__name__}: {e}")
                return fallback
            except Exception as e:
                logger.error(f"critical failure in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

def safe_type_cast(value: Any, target_type: type, default: Any = None) -> Any:
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default

def batch_process_safely(items: list, processor: Callable):
    results = []
    for item in items:
        try:
            results.append(processor(item))
        except Exception:
            results.append(None)
    return results