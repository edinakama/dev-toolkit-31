import json
import os
from typing import Any, Dict

class ConfigLoader:
    """dynamic configuration injector with fallback recursion"""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_config = json.load(f)
                self._deep_merge(self._data, user_config)
        return self

    def _deep_merge(self, base: dict, overlay: dict):
        for key, value in overlay.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

def get_config(path: str = 'settings.json') -> ConfigLoader:
    defaults = {'host': 'localhost', 'port': 8080, 'debug': False}
    return ConfigLoader(defaults).load(path)