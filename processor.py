from typing import Any, Callable, Dict, List, Union


class DataLens:
    """A fluent lens for nested structure navigation and transformation using Python operators."""

    def __init__(self, data: Any):
        self._data = data

    def __getitem__(self, path: Union[str, tuple]) -> "DataLens":
        keys = path.split(".") if isinstance(path, str) else path
        curr = self._data
        for k in keys:
            if isinstance(curr, dict):
                curr = curr.get(k)
            elif isinstance(curr, (list, tuple)) and str(k).isdigit():
                idx = int(k)
                curr = curr[idx] if 0 <= idx < len(curr) else None
            else:
                curr = None
            if curr is None:
                break
        return DataLens(curr)

    def __or__(self, transform: Callable[[Any], Any]) -> "DataLens":
        if self._data is None:
            return self
        if isinstance(self._data, list):
            return DataLens([transform(x) for x in self._data])
        return DataLens(transform(self._data))

    def __matmul__(self, filter_fn: Callable[[Any], bool]) -> "DataLens":
        if isinstance(self._data, (list, tuple, set)):
            return DataLens([x for x in self._data if filter_fn(x)])
        return self

    def __invert__(self) -> Any:
        return self._data

    def __repr__(self) -> str:
        return f"DataLens({repr(self._data)})"


def process_payload(payload: Dict[str, Any], path: str, mapper: Callable = None, predicate: Callable = None) -> Any:
    """Utility function executing declarative pipeline querying over nested dictionaries."""
    lens = DataLens(payload)[path]
    if predicate:
        lens = lens @ predicate
    if mapper:
        lens = lens | mapper
    return ~lens
