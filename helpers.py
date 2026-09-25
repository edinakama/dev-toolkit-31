import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback strategy."""
    def __init__(self, defaults: Dict[str, Any]):
        self.config = defaults.copy()

    def load_from_json(self, path: str) -> 'ConfigLoader':
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    self.config.update(json.load(f))
                except json.JSONDecodeError:
                    pass
        return self

    def load_from_env(self, prefix: str = 'APP_') -> 'ConfigLoader':
        for key in self.config:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                try:
                    self.config[key] = int(val) if val.isdigit() else val
                except ValueError:
                    self.config[key] = val
        return self

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def __repr__(self) -> str:
        return f"ConfigLoader({self.config})"