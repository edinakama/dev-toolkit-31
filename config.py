import os
import json
from collections import UserDict
from typing import Any, Dict


class ConfigLoader(UserDict):
    """Cascading configuration loader with auto-typing and dot-notation access."""

    def __init__(self, defaults: Dict[str, Any] | None = None, env_prefix: str = "DEV_"):
        super().__init__()
        self._defaults = defaults or {}
        self._env_prefix = env_prefix
        self.reload()

    def reload(self, source_file: str | None = None) -> "ConfigLoader":
        file_data = {}
        if source_file and os.path.exists(source_file):
            with open(source_file, "r", encoding="utf-8") as f:
                file_data = json.load(f)

        merged = {}
        for key, default_val in self._defaults.items():
            val = file_data.get(key, default_val)
            env_key = f"{self._env_prefix}{key.upper()}"
            if env_key in os.environ:
                val = self._cast(os.environ[env_key], type(default_val))
            merged[key] = val

        self.data = merged
        return self

    def _cast(self, raw: str, target_type: type) -> Any:
        if target_type is bool:
            return raw.lower() in ("true", "1", "yes", "on")
        try:
            return target_type(raw)
        except (ValueError, TypeError):
            return raw

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"Configuration key '{name}' not found")


def load_config(defaults: Dict[str, Any], path: str | None = None) -> ConfigLoader:
    return ConfigLoader(defaults).reload(path)
