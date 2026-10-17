import math
import sys
from typing import Any, Callable, Union


class EdgeGuard:
    """Creative decorator wrapper for swallowing and normalizing extreme edge cases."""

    def __init__(self, fallback: Any = None, coerce_types: bool = True):
        self.fallback = fallback
        self.coerce_types = coerce_types

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sanitized_args = tuple(self._sanitize(a) for a in args)
            sanitized_kwargs = {k: self._sanitize(v) for k, v in kwargs.items()}
            try:
                res = func(*sanitized_args, **sanitized_kwargs)
                return self._sanitize(res)
            except (ValueError, TypeError, ZeroDivisionError, OverflowError) as err:
                return self._salvage(func, err, *sanitized_args, **sanitized_kwargs)

        return wrapper

    def _sanitize(self, val: Any) -> Any:
        if isinstance(val, float):
            if math.isnan(val):
                return 0.0
            if math.isinf(val):
                return sys.float_info.max if val > 0 else -sys.float_info.max
        elif isinstance(val, (bytes, bytearray)):
            return val.decode("utf-8", errors="replace")
        elif isinstance(val, (list, tuple)) and len(val) == 0:
            return self.fallback if self.fallback is not None else val
        return val

    def _salvage(
        self, func: Callable[..., Any], err: Exception, *args: Any, **kwargs: Any
    ) -> Any:
        if isinstance(err, ZeroDivisionError):
            return self.fallback if self.fallback is not None else float("inf")
        if isinstance(err, OverflowError):
            return sys.maxsize
        if isinstance(err, (TypeError, ValueError)) and self.coerce_types:
            try:
                str_args = tuple(str(a) for a in args)
                return func(*str_args, **kwargs)
            except Exception:
                pass
        return self.fallback


@EdgeGuard(fallback="[SAFE_FALLBACK]")
def safe_divide_and_format(a: Union[int, float, str], b: Union[int, float, str]) -> str:
    num_a, num_b = float(a), float(b)
    res = num_a / num_b
    return f"Result: {res:.2f}"
