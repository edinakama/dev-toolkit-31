import functools
import logging
from pathlib import Path
from typing import Callable, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dev-toolkit-31')

class FileSystemOrchestrator:
    def __init__(self, root: str = '.'):
        self.root = Path(root)

    def purge_temp_files(self, pattern: str = '*.tmp') -> int:
        count = 0
        for path in self.root.rglob(pattern):
            path.unlink()
            count += 1
        return count

    def reorganize_by_extension(self, target_dir: str):
        dest = self.root / target_dir
        dest.mkdir(exist_ok=True)
        for file in self.root.iterdir():
            if file.is_file() and file.suffix:
                file.rename(dest / file.name)

def memoize_with_logging(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            logger.info(f'executing {func.__name__} with {args}')
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def batch_process(items: list, action: Callable, chunk_size: int = 5) -> list:
    return [action(items[i:i + chunk_size]) for i in range(0, len(items), chunk_size)]