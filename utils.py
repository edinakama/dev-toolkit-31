from typing import Any, Callable, Dict, List, Union


class DataLens:
    """A creative lens for querying and transforming deeply nested structures."""

    def __init__(self, data: Any = None):
        self._data = data

    def focus(self, *path: Union[str, int, Callable]) -> "DataLens":
        """Navigate nested dicts/lists using keys, indices, or predicate functions."""
        current = self._data
        for step in path:
            if current is None:
                break
            if callable(step):
                if isinstance(current, (list, tuple)):
                    current = [item for item in current if step(item)]
                elif isinstance(current, dict):
                    current = {k: v for k, v in current.items() if step(k, v)}
            elif (
                isinstance(step, int)
                and isinstance(current, (list, tuple))
                and -len(current) <= step < len(current)
            ):
                current = current[step]
            elif isinstance(current, dict):
                current = current.get(step)
            else:
                current = None
        return DataLens(current)

    def transform(self, fn: Callable[[Any], Any]) -> "DataLens":
        """Apply a function recursively to the focused target."""
        if self._data is None:
            return self

        def _apply(val):
            if isinstance(val, dict):
                return {k: _apply(v) for k, v in val.items()}
            if isinstance(val, list):
                return [_apply(v) for v in val]
            return fn(val)

        return DataLens(_apply(self._data))

    def unwrap(self, default: Any = None) -> Any:
        """Retrieve underlying value or default."""
        return self._data if self._data is not None else default

    def __repr__(self) -> str:
        return f"DataLens({repr(self._data)})"


def lens(data: Any = None) -> DataLens:
    """Helper factory for DataLens wrapper."""
    return DataLens(data)
