import functools
from typing import Any, Callable, Dict, List, Union

def cast_structure(data: Any, schema: Dict[type, Callable]) -> Any:
    """recursive transformation of data structures using type mappings"""
    if isinstance(data, dict):
        return {k: cast_structure(v, schema) for k, v in data.items()}
    if isinstance(data, list):
        return [cast_structure(i, schema) for i in data]
    
    for target_type, transform in schema.items():
        if isinstance(data, target_type):
            return transform(data)
    return data

class DataPipe:
    """functional pipeline pattern for object manipulation"""
    def __init__(self, value: Any):
        self._value = value

    def apply(self, func: Callable[[Any], Any]) -> 'DataPipe':
        self._value = func(self._value)
        return self

    def result(self) -> Any:
        return self._value

def compose_handlers(*funcs: Callable) -> Callable:
    """function composition for cleaner pipeline initialization"""
    return functools.reduce(lambda f, g: lambda x: g(f(x)), funcs)

def sanitize_payload(data: Union[dict, list]) -> Union[dict, list]:
    """stripping of null values from complex structures"""
    if isinstance(data, dict):
        return {k: sanitize_payload(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [sanitize_payload(i) for i in data if i is not None]
    return data