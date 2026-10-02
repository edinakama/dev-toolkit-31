import os
from typing import Any, Dict

class ConfigNode:
    """Enables attribute-style access to nested dictionary configurations."""
    def __init__(self, data: Dict[str, Any]):
        self.__dict__['_data'] = data

    def __getattr__(self, name: str) -> Any:
        if name not in self._data:
            raise AttributeError(f"Configuration option {name!r} is undefined")
        val = self._data[name]
        return ConfigNode(val) if isinstance(val, dict) else val

    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError("Configuration instances are read-only")

    def get(self, name: str, default: Any = None) -> Any:
        return self._data.get(name, default)

class Configuration:
    """Layered configuration container supporting bitwise merge operator."""
    def __init__(self, **defaults: Any):
        self._store = defaults

    def __or__(self, other: Dict[str, Any]) -> "Configuration":
        """Merges another dictionary, returning a new configuration state."""
        if not isinstance(other, dict):
            raise TypeError("Can only merge with a dictionary")
        merged = self._deep_merge(self._store, other)
        new_config = Configuration()
        new_config._store = merged
        return new_config

    def _deep_merge(self, base: dict, update: dict) -> dict:
        result = base.copy()
        for k, v in update.items():
            if isinstance(v, dict) and isinstance(result.get(k), dict):
                result[k] = self._deep_merge(result[k], v)
            else:
                result[k] = v
        return result

    def load_env(self, prefix: str = "APP_") -> "Configuration":
        """Extracts environment variables starting with prefix to update config."""
        env_updates: Dict[str, Any] = {}
        for key, val in os.environ.items():
            if key.startswith(prefix):
                parts = key[len(prefix):].lower().split("__")
                current = env_updates
                for part in parts[:-1]:
                    current = current.setdefault(part, {})
                current[parts[-1]] = val
        return self | env_updates

    def build(self) -> ConfigNode:
        """Finalizes configuration into an immutable, attribute-accessible object."""
        return ConfigNode(self._store)
