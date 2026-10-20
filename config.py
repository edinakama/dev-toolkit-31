import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._cfg = defaults

    def load(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                user_cfg = json.load(f)
                self._deep_merge(self._cfg, user_cfg)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def __getattr__(self, name: str) -> Any:
        return self._cfg.get(name)

    def __repr__(self) -> str:
        return f"<Config(items={len(self._cfg)})>"

def get_config(defaults: Dict[str, Any], path: str = 'config.json') -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load(path)
    return loader