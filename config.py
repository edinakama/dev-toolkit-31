import os
import json
from typing import Any, Dict, Union, Optional

class DynamicConfig:
    """Cascading configuration loader with dot-notation dynamic proxying."""
    def __init__(self, defaults: Dict[str, Any], filepath: Optional[str] = None, env_prefix: str = "APP_"):
        self._defaults = defaults
        self._env_prefix = env_prefix
        self._file_data = self._load_file(filepath) if filepath else {}

    def _load_file(self, path: str) -> Dict[str, Any]:
        if path and os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _resolve_env(self, key: str) -> Any:
        env_key = f"{self._env_prefix}{key.upper()}"
        val = os.getenv(env_key)
        if val is None:
            return None
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val

    def get(self, key: str, fallback: Any = None) -> Any:
        env_val = self._resolve_env(key)
        if env_val is not None:
            return env_val
        if key in self._file_data:
            return self._file_data[key]
        return self._defaults.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"Invalid access to private property '{name}'")
        val = self.get(name)
        if isinstance(val, dict):
            return DynamicConfig(val, env_prefix=f"{self._env_prefix}{name.upper()}_")
        return val

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def load_config(filepath: Optional[str] = None, **overrides: Any) -> DynamicConfig:
    schema_defaults = {
        "host": "127.0.0.1",
        "port": 8080,
        "debug": False,
        "log_level": "INFO",
        "workers": 4,
    }
    schema_defaults.update(overrides)
    return DynamicConfig(schema_defaults, filepath)