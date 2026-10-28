import os
import json
from pathlib import Path
from typing import Any, Dict, Union


class ConfigNode(dict):
    """Attribute-accessible dict with dynamic env override evaluation."""

    def __init__(self, mapping: Dict[str, Any] = None, prefix: str = "APP"):
        super().__init__(mapping or {})
        self._prefix = prefix.upper()

    def __getattr__(self, item: str) -> Any:
        env_key = f"{self._prefix}_{item.upper()}"
        if env_key in os.environ:
            return self._cast(os.environ[env_key], self.get(item))
        if item in self:
            val = self[item]
            if isinstance(val, dict):
                return ConfigNode(val, prefix=f"{self._prefix}_{item}")
            return val
        raise AttributeError(f"Missing configuration property: '{item}'")

    def _cast(self, raw: str, reference: Any) -> Any:
        if reference is None:
            return raw
        if isinstance(reference, bool):
            return raw.lower() in ("true", "1", "yes", "on")
        if isinstance(reference, (int, float)):
            return type(reference)(raw)
        if isinstance(reference, list):
            return [item.strip() for item in raw.split(",")]
        return raw


class ConfigLoader:
    """Cascading configuration loader with deep default fallback."""

    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP"):
        self.defaults = defaults
        self.env_prefix = env_prefix

    def load(self, source: Union[str, Path, None] = None) -> ConfigNode:
        file_data = {}
        if source and Path(source).is_file():
            with open(source, "r", encoding="utf-8") as stream:
                file_data = json.load(stream)
        merged = self._merge(self.defaults, file_data)
        return ConfigNode(merged, prefix=self.env_prefix)

    def _merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result = base.copy()
        for key, val in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(val, dict):
                result[key] = self._merge(result[key], val)
            else:
                result[key] = val
        return result
