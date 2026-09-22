import re
from typing import Any, List, Dict

class Pathfinder:
    """Helper for traversing deeply nested structures using wildcard and regex patterns."""
    def __init__(self, data: Any):
        self.data = data

    def query(self, path: str) -> List[Any]:
        """Query path like 'users.*.profile.r(email|phone)'."""
        return self._find(self.data, path.split('.'))

    def _find(self, target: Any, segments: List[str]) -> List[Any]:
        if not segments:
            return [target] if target is not None else []
        
        head, *tail = segments
        results = []

        if isinstance(target, dict):
            keys = []
            if head == '*':
                keys = list(target.keys())
            elif head.startswith('r(') and head.endswith(')'):
                rx = re.compile(head[2:-1])
                keys = [k for k in target.keys() if rx.search(str(k))]
            elif head in target:
                keys = [head]
            
            for k in keys:
                results.extend(self._find(target[k], tail))
        
        elif isinstance(target, (list, tuple)):
            if head == '*':
                for item in target:
                    results.extend(self._find(item, tail))
            elif head.isdigit() and int(head) < len(target):
                results.extend(self._find(target[int(head)], tail))
                
        return results


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flattens a nested dictionary, compounding keys with an optional separator."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
