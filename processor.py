from typing import Any, Callable, Dict, List, Union


class NestedMapProcessor:
    """Nested dictionary processor supporting pipeline operations."""

    def __init__(self, data: Union[Dict, List]):
        self._data = data

    @property
    def raw(self) -> Union[Dict, List]:
        return self._data

    def flatten(self, sep: str = ".") -> Dict[str, Any]:
        """Flattens nested structures into path-keyed mapping using generators."""

        def _generator(obj: Any, prefix: str = ""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    yield from _generator(v, f"{prefix}{k}{sep}" if prefix else f"{k}{sep}")
            elif isinstance(obj, list):
                for idx, v in enumerate(obj):
                    yield from _generator(v, f"{prefix}{idx}{sep}" if prefix else f"{idx}{sep}")
            else:
                yield prefix.rstrip(sep), obj

        return dict(_generator(self._data))

    def unflatten(self, sep: str = ".") -> Dict[str, Any]:
        """Reconstructs nested structures from flat path mappings."""
        flat_data = self._data if isinstance(self._data, dict) else self.flatten(sep=sep)
        result: Dict[str, Any] = {}

        for key, value in flat_data.items():
            parts = str(key).split(sep)
            curr = result
            for part in parts[:-1]:
                curr = curr.setdefault(part, {})
            curr[parts[-1]] = value

        return result

    def mutate_leaves(self, predicate: Callable[[Any], bool], transform: Callable[[Any], Any]) -> "NestedMapProcessor":
        """Recursively applies transform logic to matching leaf nodes."""

        def _mutate(node: Any) -> Any:
            if isinstance(node, dict):
                return {k: _mutate(v) for k, v in node.items()}
            elif isinstance(node, list):
                return [_mutate(v) for v in node]
            return transform(node) if predicate(node) else node

        return NestedMapProcessor(_mutate(self._data))

    def __rshift__(self, func: Callable[[Any], Any]) -> "NestedMapProcessor":
        """Enables functional syntax using standard shift pipeline operator."""
        return NestedMapProcessor(func(self._data))


def morph_data(data: Dict[str, Any], operations: List[Callable]) -> Dict[str, Any]:
    """Applies sequential processing operations over arbitrary dict shapes."""
    proc = NestedMapProcessor(data)
    for op in operations:
        proc = proc >> op
    return proc.raw