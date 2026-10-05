import os
import json
import logging

class ConfigLoader:
    """Dynamic config handler with defensive fallbacks."""
    def __init__(self, path: str = 'settings.json'):
        self.path = path
        self.data = {}

    def load(self) -> dict:
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"missing {self.path}")
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            logging.warning(f"config loading failure: {e}. applying emergency defaults.")
            self.data = self._get_emergency_defaults()
        return self.data

    def _get_emergency_defaults(self) -> dict:
        return {"env": "sandbox", "retries": 3, "timeout": 30.0}

    def get_safe(self, key: str, fallback=None):
        """Access nested keys with dot notation."""
        keys = key.split('.')
        val = self.data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return fallback

loader = ConfigLoader()