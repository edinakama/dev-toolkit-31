import time
import random
import math
from typing import Callable, Iterable, Type, Tuple, Any, Optional


def fibonacci_jitter_backoff(base_delay: float = 1.0, max_delay: float = 60.0) -> Iterable[float]:
    a, b = base_delay, base_delay
    phi = (1 + math.sqrt(5)) / 2
    while True:
        jitter = random.uniform(1.0, phi)
        yield min(a * jitter, max_delay)
        a, b = b, a + b


class ResilientNetworkOperation:
    def __init__(
        self,
        retries: int = 3,
        backoff_gen: Optional[Iterable[float]] = None,
        exceptions: Tuple[Type[BaseException], ...] = (Exception,)
    ):
        self.retries = retries
        self.backoff_gen = backoff_gen or fibonacci_jitter_backoff()
        self.exceptions = exceptions

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = iter(self.backoff_gen)
            last_err = None
            for attempt in range(1, self.retries + 2):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as err:
                    last_err = err
                    if attempt > self.retries:
                        break
                    time.sleep(next(delays))
            raise RuntimeError(f"Operation failed after {self.retries} retries") from last_err
        return wrapper


def retry_network_op(retries: int = 3, exceptions: Tuple[Type[BaseException], ...] = (Exception,)):
    return ResilientNetworkOperation(retries=retries, exceptions=exceptions)
