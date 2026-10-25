import random
import time
from functools import wraps
from typing import Callable, Any, Type, Sequence


def dynamic_backoff(base_delay: float = 1.0, factor: float = 2.0, max_delay: float = 60.0):
    """Generator yielding jittered exponential backoff intervals."""
    delay = base_delay
    while True:
        jitter = (random.random() - 0.5) * 0.2 * delay
        yield min(max_delay, max(0.1, delay + jitter))
        delay *= factor


def resilient_network_op(
    retries: int = 3,
    exceptions: Sequence[Type[BaseException]] = (Exception,),
    base_delay: float = 0.5,
    on_retry: Callable[[BaseException, int, float], None] | None = None
):
    """Decorator applying dynamic backoff and retry strategy to network operations."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff_gen = dynamic_backoff(base_delay=base_delay)
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as err:
                    if attempt == retries:
                        raise err
                    delay = next(backoff_gen)
                    if on_retry:
                        on_retry(err, attempt, delay)
                    time.sleep(delay)
        return wrapper
    return decorator
