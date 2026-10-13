import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, path: str) -> 'ConfigLoader':
        file = Path(path)
        if file.exists():
            try:
                with open(file, 'r') as f:
                    self._data.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def items(self):
        return self._data.items()

def get_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    return loader.load(path)

# Usage example:
# cfg = get_config('settings.json', {'debug': False, 'port': 8080})
# print(cfg.port)