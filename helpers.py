import time
import functools
from typing import Callable, Any, TypeVar

T = TypeVar('T')

def time_execution(func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'[dev-toolkit-31] {func.__name__} finished in {time.perf_counter() - start:.4f}s')
        return result
    return wrapper

def retry_operation(attempts: int = 3, delay: float = 0.5) -> Callable: 
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_err = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay * (2 ** i))
            raise last_err
        return wrapper
    return decorator

def memoize_instance(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper