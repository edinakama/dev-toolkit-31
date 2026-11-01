import json
import os
from pathlib import Path
from typing import Any, Dict, Union, Optional


class ConfigLoader:
    """Dynamic configuration loader with default cascading and env overrides."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self._defaults = defaults or {}
        self._store: Dict[str, Any] = {}

    def load_dict(self, data: Dict[str, Any]) -> "ConfigLoader":
        self._store.update(data)
        return self

    def load_json(self, path: Union[str, Path]) -> "ConfigLoader":
        file_path = Path(path)
        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as f:
                self._store.update(json.load(f))
        return self

    def _fetch(self, key: str) -> Any:
        env_var = f"CONFIG_{key.upper()}"
        if env_var in os.environ:
            raw = os.environ[env_var]
            if raw.isdigit():
                return int(raw)
            if raw.lower() in ("true", "false"):
                return raw.lower() == "true"
            return raw

        if key in self._store:
            val = self._store[key]
        elif key in self._defaults:
            val = self._defaults[key]
        else:
            raise KeyError(f"Configuration option '{key}' is undefined")

        if isinstance(val, dict):
            sub_defaults = self._defaults.get(key, {})
            if not isinstance(sub_defaults, dict):
                sub_defaults = {}
            return ConfigLoader(sub_defaults).load_dict(val)
        return val

    def __getattr__(self, name: str) -> Any:
        try:
            return self._fetch(name)
        except KeyError as err:
            raise AttributeError(err) from err

    def __getitem__(self, item: str) -> Any:
        return self._fetch(item)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self._fetch(key)
        except KeyError:
            return default
