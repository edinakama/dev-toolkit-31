from typing import Any, Union, Callable

class Navigator:
    """A fluent and safe object navigation utility utilizing operator overloading."""
    def __init__(self, obj: Any):
        self._obj = obj

    def __truediv__(self, key: Union[str, int, Callable[[Any], Any]]) -> "Navigator":
        if self._obj is None:
            return self
        try:
            if callable(key) and not isinstance(key, type):
                return Navigator(key(self._obj))
            if isinstance(self._obj, dict):
                return Navigator(self._obj.get(key))  # type: ignore
            if isinstance(self._obj, (list, tuple)):
                return Navigator(self._obj[int(key)])  # type: ignore
            return Navigator(getattr(self._obj, str(key), None))
        except (IndexError, KeyError, ValueError, AttributeError, TypeError):
            return Navigator(None)

    def resolve(self, default: Any = None) -> Any:
        """Unwraps the final navigated value or returns the default fallback."""
        return default if self._obj is None else self._obj

    def __repr__(self) -> str:
        return f"Navigator({self._obj!r})"


def dot_path(target: Any, path: str, default: Any = None) -> Any:
    """Helper to navigate via a dot-separated string path."""
    nav = Navigator(target)
    for part in path.split('.'):
        if part.isdigit():
            nav = nav / int(part)
        else:
            nav = nav / part
    return nav.resolve(default)
