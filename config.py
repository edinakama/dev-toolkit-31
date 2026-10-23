import os
from typing import Any, Dict

class ConfigStore:
    """Dynamic dictionary wrapper for environment configurations"""
    def __init__(self, prefix: str = "DEV_TOOKIT_"):
        self._prefix = prefix
        self._data = {k[len(prefix):]: v for k, v in os.environ.items() if k.startswith(prefix)}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key.upper(), default)

    def __getattr__(self, item: str) -> Any:
        val = self.get(item)
        if val is None:
            raise AttributeError(f"Config key '{item}' not found")
        return val

    def registry_dump(self) -> Dict[str, str]:
        return {k.lower(): v for k, v in self._data.items()}

def load_settings() -> ConfigStore:
    return ConfigStore()

# Execution entry for runtime validation
if __name__ == "__main__":
    cfg = load_settings()
    print(f"Toolkit state initialized: {len(cfg.registry_dump())} keys loaded")