from typing import Any, Callable, Mapping, Sequence

class Flow:
    """Pipeline processor leveraging the bitwise OR operator for execution flow."""
    def __init__(self, value: Any):
        self.value = value

    def __or__(self, func: Callable[[Any], Any]) -> "Flow":
        return Flow(func(self.value))

    def __repr__(self) -> str:
        return f"Flow({self.value!r})"


class PathFinder:
    """Safe retrieval of deep-nested structure elements via string-based paths."""
    def __init__(self, target: Any, separator: str = "."):
        self.target = target
        self.separator = separator

    def resolve(self, path: str, fallback: Any = None) -> Any:
        keys = path.split(self.separator)
        current = self.target
        for key in keys:
            if isinstance(current, Mapping) and key in current:
                current = current[key]
            elif isinstance(current, Sequence) and not isinstance(current, (str, bytes)) and key.isdigit():
                idx = int(key)
                current = current[idx] if 0 <= idx < len(current) else fallback
            else:
                return fallback
        return current


def coalesce(*args: Any) -> Any:
    """Returns the first non-None argument encountered."""
    return next((x for x in args if x is not None), None)
