import functools
from typing import Any, Callable, Dict, Optional

def pipeline(*funcs: Callable) -> Callable:
    """Compose functions into a data transformation pipe."""
    def wrapper(data: Any) -> Any:
        return functools.reduce(lambda v, f: f(v), funcs, data)
    return wrapper

def recursive_map(func: Callable, data: Any) -> Any:
    """Deep apply function to values in nested containers."""
    if isinstance(data, dict):
        return {k: recursive_map(func, v) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        return [recursive_map(func, i) for i in data]
    return func(data)

class DataSanitizer:
    """Sanitization routines for arbitrary input structures."""
    def __init__(self, default: Any = None):
        self.default = default

    def clean(self, data: Any, schema: Optional[Dict] = None) -> Any:
        if not schema:
            return data
        
        def apply_rule(val: Any) -> Any:
            rule = schema.get(type(val), lambda x: x)
            try:
                return rule(val)
            except Exception:
                return self.default
        
        return recursive_map(apply_rule, data)