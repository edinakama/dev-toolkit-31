import os
import json
from pathlib import Path
from typing import Any, Union


class DynamicConfig(dict):
    """Flexible configuration node supporting attribute access and operator merging."""

    def __init__(self, defaults: dict[str, Any] | None = None, **overrides: Any):
        base = defaults or {}
        merged = {**base, **overrides}
        super().__init__()
        for key, val in merged.items():
            self[key] = DynamicConfig(val) if isinstance(val, dict) else val

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"Configuration key '{name}' not found") from None

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = DynamicConfig(value) if isinstance(value, dict) else value

    def __or__(self, other: Any) -> "DynamicConfig":
        if not isinstance(other, dict):
            return self
        new_cfg = DynamicConfig(dict(self))
        for k, v in other.items():
            if k in new_cfg and isinstance(new_cfg[k], DynamicConfig) and isinstance(v, dict):
                new_cfg[k] = new_cfg[k] | v
            else:
                new_cfg[k] = DynamicConfig(v) if isinstance(v, dict) else v
        return new_cfg


def load_config(
    file_path: Union[str, Path, None] = None,
    defaults: dict[str, Any] | None = None,
    env_prefix: str = "APP_",
) -> DynamicConfig:
    """Loads config from defaults, JSON file, and environment overrides."""
    base_defaults = defaults or {
        "app": {"name": "dev-toolkit", "debug": False, "port": 8080},
        "logging": {"level": "INFO", "format": "json\