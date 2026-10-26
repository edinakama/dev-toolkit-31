import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict, Union


class DeepChainConfig:
    """Nested configuration loader using ChainMap with env variable overlays."""

    def __init__(self, primary: Dict[str, Any] = None, defaults: Dict[str, Any] = None):
        self._primary = primary if primary is not None else {}
        self._defaults = defaults if defaults is not None else {}
        self._map = ChainMap(self._primary, self._defaults)

    def __getattr__(self, name: str) -> Any:
        env_key = name.upper()
        if env_key in os.environ:
            return self._coerce(os.environ[env_key])

        if name not in self._map:
            raise AttributeError(f"Missing configuration key: {name}")

        val = self._map[name]
        if isinstance(val, dict):
            def_sub = self._defaults.get(name, {}) if isinstance(self._defaults.get(name), dict) else {}
            return DeepChainConfig(val, def_sub)
        return val

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    @staticmethod
    def _coerce(val: str) -> Any:
        if val.lower() in ("true", "false"):
            return val.lower() == "true"
        for cast in (int, float):
            try:
                return cast(val)
            except ValueError:
                pass
        return val

    def load_file(self, filepath: Union[str, Path]) -> "DeepChainConfig":
        path = Path(filepath)
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                self._primary.update(json.load(f))
        return self


def create_config(filepath: Union[str, Path] = None, defaults: Dict[str, Any] = None) -> DeepChainConfig:
    cfg = DeepChainConfig(defaults=defaults or {})
    if filepath:
        cfg.load_file(filepath)
    return cfg
