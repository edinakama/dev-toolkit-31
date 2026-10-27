import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def load_json(self, filepath: str) -> 'ConfigLoader':
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                loaded = json.load(f)
                self._data.update({k: v for k, v in loaded.items() if k in self._data})
        return self

    def env_override(self, prefix: str = 'APP_') -> 'ConfigLoader':
        for key in self._data.keys():
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val is not None:
                self._data[key] = type(self._data[key])(env_val)
        return self

    def to_dict(self) -> Dict[str, Any]:
        return self._data

if __name__ == '__main__':
    defaults = {'port': 8080, 'debug': False}
    cfg = ConfigLoader(defaults).load_json('config.json').env_override()
    print(f"Active port: {cfg.port}")