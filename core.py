import sys
import traceback
from typing import Any, Callable, TypeVar, Optional

T = TypeVar('T')

class ToolkitError(Exception):
    def __init__(self, message: str, original: Optional[Exception] = None):
        super().__init__(message)
        self.original = original

def resilient_execute(func: Callable[..., T], *args: Any, fallback: Optional[T] = None, **kwargs: Any) -> Optional[T]:
    try:
        return func(*args, **kwargs)
    except ZeroDivisionError as zde:
        sys.stderr.write(f"⚠️ Mathematical anomaly neutralized: {zde}\n")
        return fallback
    except (TypeError, ValueError) as err:
        sys.stderr.write(f"⚠️ Type/Value disturbance caught: {err}\n")
        return fallback
    except Exception as exc:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_list = traceback.format_tb(exc_tb)
        clean_tb = "".join(tb_list).strip()
        sys.stderr.write(f"💥 Unforeseen singularity in {func.__name__}: {exc}\nTraceback:\n{clean_tb}\n")
        raise ToolkitError(f"Critical failure in {func.__name__}", original=exc) from exc
    finally:
        sys.stderr.flush()