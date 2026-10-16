import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    """dynamic configuration loader with recursive default injection"""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> Dict[str, Any]:
        file_path = Path(path)
        if not file_path.exists():
            return self._data
        
        with open(file_path, 'r') as f:
            user_config = json.load(f)
            return self._merge(self._data, user_config)

    def _merge(self, base: Any, over: Any) -> Any:
        if isinstance(base, dict) and isinstance(over, dict):
            return {k: self._merge(base.get(k, {}), over.get(k, {})) 
                    for k in set(base) | set(over)}
        return over if over is not None else base

def get_config_handler(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults)

# Usage example:
# loader = get_config_handler({'host': 'localhost', 'port': 8080})
# config = loader.load('config.json')