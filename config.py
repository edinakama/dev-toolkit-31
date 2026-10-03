import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._deep_merge(self._data, file_data)

    def _deep_merge(self, base: Dict, overrides: Dict) -> None:
        for key, value in overrides.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        val = self._data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    @classmethod
    def from_env(cls, prefix: str, schema: Dict[str, Any]) -> 'ConfigLoader':
        loader = cls(schema)
        for key in schema:
            env_val = os.getenv(f"{prefix}_{key.upper()}")
            if env_val:
                loader._data[key] = env_val
        return loader