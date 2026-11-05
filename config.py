import os
from typing import Any, Callable, Dict, Optional, Type, TypeVar

T = TypeVar("T")


class ConfigVar:
    """A descriptor mapping environment variables to typed attributes.

    Evaluates environment values lazily upon access and coerces them into
    expected target types using custom transformations.
    """

    def __init__(
        self, key: str, default: Any = None, cast: Optional[Callable[[str], Any]] = None
    ) -> None:
        self.key: str = key
        self.default: Any = default
        self.cast: Optional[Callable[[str], Any]] = cast

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> Any:
        raw_value: Optional[str] = os.getenv(self.key)
        if raw_value is None:
            return self.default
        if self.cast is not None:
            try:
                return self.cast(raw_value)
            except (ValueError, TypeError):
                return self.default
        return raw_value


class DynamicConfig:
    """Dynamic key-value configuration wrapper supporting dynamic fallbacks.

    Provides attribute-based retrieval, environmental overrides, and full export capabilities.
    """

    debug: ConfigVar = ConfigVar("APP_DEBUG", default=False, cast=lambda v: v.lower() in ("true", "1", "yes"))
    port: ConfigVar = ConfigVar("APP_PORT", default=8080, cast=int)
    secret_key: ConfigVar = ConfigVar("APP_SECRET", default="dev-secret-key-31")

    def __init__(self, **overrides: Any) -> None:
        self._overrides: Dict[str, Any] = overrides

    def __getitem__(self, item: str) -> Any:
        if item in self._overrides:
            return self._overrides[item]
        return getattr(self, item, None)

    def dump(self) -> Dict[str, Any]:
        """Export current active configuration state into a single dictionary."""
        cls_type = type(self)
        known_keys = [attr for attr in dir(cls_type) if isinstance(getattr(cls_type, attr), ConfigVar)]
        base_config = {key: getattr(self, key) for key in known_keys}
        return {**base_config, **self._overrides}
