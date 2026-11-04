import collections
from typing import Any, Iterable, Dict, Union

def morph(data: Any, path: str = '/', sep: str = '.') -> Any:
    """Traverse nested structures using dot-notation strings."""
    keys = path.strip(sep).split(sep)
    current = data
    for key in keys:
        if not key: continue
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, (list, tuple)) and key.isdigit():
            idx = int(key)
            current = current[idx] if idx < len(current) else None
        else:
            return None
    return current

def deep_flatten(items: Iterable) -> Iterable:
    """Recursive generator for flattening heterogeneous nested containers."""
    for item in items:
        if isinstance(item, (list, tuple, set)) and not isinstance(item, (str, bytes)):
            yield from deep_flatten(item)
        else:
            yield item

def smart_dict_merge(*dicts: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursive merge for dictionary structures."""
    result = collections.defaultdict(dict)
    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict) and k in result and isinstance(result[k], dict):
                result[k] = smart_dict_merge(result[k], v)
            else:
                result[k] = v
    return dict(result)