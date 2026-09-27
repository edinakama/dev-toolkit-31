import os
import json
from typing import Any, Dict

class ConfigLoader:
    """A dynamically layered configuration loader with fallback defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._storage = defaults.copy()

    def __getattr__(self, name: str) -> Any:
        return self._storage.get(name)

    def ingest_env(self, prefix: str = 'APP_'):
        for key, value in os.environ.items():
            if key.startswith(prefix):
                normalized = key[len(prefix):].lower()
                self._storage[normalized] = self._try_cast(value)

    def ingest_json(self, path: str):
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._storage.update(json.load(f))

    @staticmethod
    def _try_cast(value: str) -> Any:
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        try:
            return int(value) if '.' not in value else float(value)
        except ValueError:
            return value

def get_config(defaults: Dict[str, Any] = None) -> ConfigLoader:
    loader = ConfigLoader(defaults or {})
    loader.ingest_env()
    return loader