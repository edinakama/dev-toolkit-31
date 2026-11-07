import sys
import math
from typing import Callable, Any, Dict, Optional


class EdgeCaseGuard:
    """Dynamic resilience wrapper handling extreme inputs and runtime anomalies."""

    DEFAULT_FALLBACKS: Dict[type, Any] = {
        ZeroDivisionError: float("nan"),
        OverflowError: sys.float_info.max,
        RecursionError: None,
        TypeError: "",
        ValueError: None,
        KeyError: None,
        IndexError: None,
    }

    def __init__(self, custom_fallbacks: Optional[Dict[type, Any]] = None):
        self.fallbacks = {**self.DEFAULT_FALLBACKS, **(custom_fallbacks or {})}

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sanitized_args = tuple(self._sanitize(a) for a in args)
            sanitized_kwargs = {k: self._sanitize(v) for k, v in kwargs.items()}

            try:
                res = func(*sanitized_args, **sanitized_kwargs)
                return self._sanitize(res)
            except Exception as exc:
                for exc_type, fallback in self.fallbacks.items():
                    if isinstance(exc, exc_type):
                        if callable(fallback):
                            return fallback(exc, *args, **kwargs)
                        return fallback
                raise exc

        return wrapper

    def _sanitize(self, value: Any) -> Any:
        """Neutralize radioactive edge case values like Inf, NaN, and deep nesting."""
        if isinstance(value, float):
            if math.isnan(value):
                return 0.0
            if math.isinf(value):
                return sys.float_info.max if value > 0 else -sys.float_info.max
        elif isinstance(value, (list, tuple)):
            return type(value)(self._sanitize(v) for v in value)
        elif isinstance(value, dict):
            return {k: self._sanitize(v) for k, v in value.items()}
        return value


def safe_execute(target_func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    guard = EdgeCaseGuard()
    return guard(target_func)(*args, **kwargs)
