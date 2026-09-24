import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._deep_update(self._data, file_data)

    def _deep_update(self, base: Dict, patch: Dict) -> None:
        for key, value in patch.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __repr__(self) -> str:
        return f"ConfigStore({self._data})"

def load_app_config(config_path: str = "config.json") -> ConfigLoader:
    defaults = {"port": 8080, "debug": False, "db": {"host": "localhost"}}
    loader = ConfigLoader(defaults)
    loader.load(config_path)
    return loader