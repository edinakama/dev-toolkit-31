from typing import Any, Callable, Dict, List, Union
from functools import reduce
import operator

def deep_reach(data: Dict, path: str, default: Any = None) -> Any:
    """Navigates nested dictionaries using dot-notation keys."""
    try:
        return reduce(operator.getitem, path.split('.'), data)
    except (KeyError, TypeError, AttributeError):
        return default

def batch_transform(data: List[Dict], pipeline: List[Callable]) -> List[Any]:
    """Sequential application of functions over dataset."""
    return [reduce(lambda v, func: func(v), pipeline, item) for item in data]

def dict_flatten(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    """Flattens arbitrary nested structures into single level."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(dict_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def sanitize_payload(data: Union[Dict, List], allowed_types: tuple = (str, int, float, bool)) -> Any:
    """Recursive type filtering for serialization safety."""
    if isinstance(data, dict):
        return {k: sanitize_payload(v, allowed_types) for k, v in data.items() if isinstance(v, allowed_types + (dict, list))}
    if isinstance(data, list):
        return [sanitize_payload(i, allowed_types) for i in data if isinstance(i, allowed_types + (dict, list))]
    return data if isinstance(data, allowed_types) else None