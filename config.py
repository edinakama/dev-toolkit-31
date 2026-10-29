import os
import logging
from typing import Any, Dict

class ConfigError(Exception):
    pass

def load_environment_variable(key: str, default: Any = None) -> Any:
    try:
        value = os.environ.get(key)
        if value is None:
            if default is None:
                raise ConfigError(f"Missing critical config: {key}")
            return default
        return type(default)(value) if default is not None else value
    except (ValueError, TypeError) as e:
        logging.error(f"Malformed configuration for {key}: {e}")
        return default

def validate_config_schema(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
    try:
        return all(isinstance(data.get(k), t) for k, t in schema.items())
    except AttributeError:
        return False

class DevToolkitConfig:
    def __init__(self, settings: Dict[str, Any]):
        self._settings = settings

    def __getitem__(self, key: str) -> Any:
        if key not in self._settings:
            raise KeyError(f"Key {key} absent in toolkit config")
        return self._settings[key]

    def safe_get(self, key: str, fallback: Any = None) -> Any:
        return self._settings.get(key, fallback)

# Initialization of global config container
def initialize_config() -> DevToolkitConfig:
    try:
        raw_data = {"version": "3.1.0", "debug": True}
        return DevToolkitConfig(raw_data)
    except Exception as e:
        logging.critical(f"Initialization sequence failed: {e}")
        return DevToolkitConfig({})