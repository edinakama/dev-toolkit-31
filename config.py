import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_config = json.load(f)
                self._data.update({k: v for k, v in user_config.items() if k in self._data})

    def merge_env(self, prefix: str = 'APP_') -> None:
        for key in self._data.keys():
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val:
                try:
                    self._data[key] = type(self._data[key])(env_val)
                except (ValueError, TypeError):
                    pass

    def export(self) -> Dict[str, Any]:
        return self._data

def load_app_config(path: str = 'config.json') -> ConfigLoader:
    defaults = {'host': '127.0.0.1', 'port': 8080, 'debug': False}
    cfg = ConfigLoader(defaults)
    cfg.load_from_json(path)
    cfg.merge_env()
    return cfg