import inspect
from typing import Callable, Dict, Any, List, Optional


class UtilityNamespace:
    """Dynamic namespace container for reorganized utility functions."""

    def __init__(self, name: str):
        self._name = name
        self._funcs: Dict[str, Callable] = {}

    def register(self, alias: Optional[str] = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            fn_name = alias or func.__name__
            self._funcs[fn_name] = func
            setattr(self, fn_name, func)
            return func
        return decorator

    def batch_process(self, data: List[Any], func_name: str) -> List[Any]:
        if func_name not in self._funcs:
            raise AttributeError(f"Function '{func_name}' not registered in {self._name}")
        target = self._funcs[func_name]
        return [target(item) for item in data]


text_utils = UtilityNamespace("text")
dict_utils = UtilityNamespace("dict")


@text_utils.register(alias="sanitize")
def clean_string(value: str) -> str:
    return " ".join(str(value).strip().split())


@text_utils.register(alias="slugify")
def create_slug(value: str) -> str:
    return "-".join(clean_string(value).lower().split())


@dict_utils.register(alias="flatten")
def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
