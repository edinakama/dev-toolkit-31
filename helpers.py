import inspect
from typing import Callable, Any, List

class Flow:
    """A creative pipelines helper allowing functional chaining via operators."""
    def __init__(self, value: Any = None):
        self._value = value
        self._steps: List[Callable] = []

    def __or__(self, other: Callable[[Any], Any]) -> 'Flow':
        if not callable(other):
            raise TypeError("Flow step must be a callable.")
        new_flow = Flow(self._value)
        new_flow._steps = self._steps + [other]
        return new_flow

    def __rshift__(self, other: Any) -> Any:
        """Evaluates the pipeline with the provided initial input."""
        val = other if self._value is None else self._value
        for step in self._steps:
            sig = inspect.signature(step)
            params = list(sig.parameters.values())
            if len(params) == 0:
                val = step()
            else:
                val = step(val)
        return val

    def execute(self) -> Any:
        return self >> self._value

def safeguard(default_value: Any):
    """Decorator helper to wrap functions in a try-except returning default."""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_value
        return wrapper
    return decorator

to_upper = safeguard("")(lambda s: str(s).upper())
to_words = safeguard([])(lambda s: str(s).split())
slugify = safeguard("")(lambda s: "-".join(str(s).lower().split()))
