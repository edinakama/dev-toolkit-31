import random
import time
from typing import Callable, Any, Tuple, Optional


def _fibonacci_jitter_sequence(base: float, max_delay: float):
    a, b = 1, 1
    while True:
        delay = min(base * a + random.uniform(0, base), max_delay)
        yield delay
        a, b = b, a + b


class NetworkRetryExhausted(Exception):
    """Raised when all retry attempts fail."""
    pass


def resilient_network_op(
    retries: int = 4,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    retryable_exceptions: Tuple[type, ...] = (Exception,)
) -> Callable:
    """Decorator applying Fibonacci jitter backoff to network calls."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay_gen = _fibonacci_jitter_sequence(base_delay, max_delay)
            last_exception: Optional[BaseException] = None

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    last_exception = exc
                    if attempt == retries:
                        break
                    wait_time = next(delay_gen)
                    time.sleep(wait_time)

            raise NetworkRetryExhausted(
                f"Operation '{func.__name__}' failed after {retries} attempts"
            ) from last_exception

        return wrapper
    return decorator
