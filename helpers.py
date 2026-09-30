import functools
from typing import Any, Callable, Dict, Type

class LoopValidationError(ValueError):
    """Exception raised when incoming processing loop inputs fail validation."""
    pass

class ValidatedGeneratorProxy:
    """Proxies a generator to validate values sent into the loop."""

    def __init__(self, target_gen: Any, schema: Dict[str, Type]):
        self.target_gen = target_gen
        self.schema = schema

    def __iter__(self):
        return self

    def __next__(self) -> Any:
        return self.send(None)

    def send(self, value: Any) -> Any:
        if value is not None:
            if not isinstance(value, dict):
                raise LoopValidationError(
                    f"Processing loop input must be a dict, got {type(value).__name__}"
                )
            for key, expected_type in self.schema.items():
                if key not in value:
                    raise LoopValidationError(f"Missing required key: '{key}'")
                val = value[key]
                if not isinstance(val, expected_type):
                    raise LoopValidationError(
                        f"Key '{key}' must be {expected_type.__name__}, got {type(val).__name__}"
                    )
        return self.target_gen.send(value)

    def throw(self, typ: Type[BaseException], val: Any = None, tb: Any = None) -> Any:
        return self.target_gen.throw(typ, val, tb)

    def close(self) -> None:
        self.target_gen.close()

def validated_loop(schema: Dict[str, Type]) -> Callable:
    """
    Decorator to wrap a generator-based processing loop.
    Enforces that inputs sent via .send() match the expected schema types.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> ValidatedGeneratorProxy:
            return ValidatedGeneratorProxy(func(*args, **kwargs), schema)
        return wrapper
    return decorator