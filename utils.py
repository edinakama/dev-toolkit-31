import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-31')

class ExecutionContext:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        logger.info(f"context {self.name} duration: {elapsed:.4f}s")

def batch_process(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        items = args[0] if args else []
        return [func(item, **kwargs) for item in items]
    return wrapper

def dynamic_filter(data: list[dict], key: str, value: Any) -> list[dict]:
    return [item for item in data if item.get(key) == value]

def clean_nones(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}

def format_byte_size(num: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if num < 1024:
            return f"{num:.1f}{unit}"
        num /= 1024
    return f"{num:.1f}TB"