import collections.abc
from typing import Any, Callable, Dict, List


class StreamTransformer:
    """Data processor using pipe operator for flexible nested transformations."""

    def __init__(self, step: Callable[[Any], Any]):
        self.step = step

    def __ror__(self, data: Any) -> Any:
        return self._apply(data)

    def __or__(self, next_step: "StreamTransformer") -> "StreamTransformer":
        return StreamTransformer(lambda d: next_step.step(self.step(d)))

    def _apply(self, data: Any) -> Any:
        if isinstance(data, list):
            return [self._apply(item) for item in data]
        if isinstance(data, dict):
            return {k: self._apply(v) for k, v in data.items()}
        return self.step(data)


def pluck(*keys: str) -> StreamTransformer:
    """Filter dict objects inside stream to contain only specific keys."""

    def _pluck(val: Any) -> Any:
        if isinstance(val, dict):
            return {k: v for k, v in val.items() if k in keys}
        return val

    return StreamTransformer(_pluck)


def morph(target_type: type, fallback: Any = None) -> StreamTransformer:
    """Cast atomic values to target type with safe fallback."""

    def _morph(val: Any) -> Any:
        try:
            return target_type(val)
        except (ValueError, TypeError):
            return fallback if fallback is not None else val

    return StreamTransformer(_morph)


def flatten_dict(data: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dict into dot-notation map."""
    flat: Dict[str, Any] = {}

    def _recursive_flatten(obj: Any, prefix: str = ""):
        if isinstance(obj, collections.abc.Mapping):
            for k, v in obj.items():
                p = f"{prefix}{sep}{k}" if prefix else str(k)
                _recursive_flatten(v, p)
        else:
            flat[prefix] = obj

    _recursive_flatten(data)
    return flat
