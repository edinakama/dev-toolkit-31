import random
import time
from typing import Callable, Any, Type, Sequence, Generator

def _golden_jitter_backoff(base: float, cap: float) -> Generator[float, None, None]:
    """Generates delays using golden ratio scaling and random jitter."""
    phi = 1.61803398875
    current = base
    while True:
        jittered = current * (0.8 + random.random() * 0.4)
        yield min(cap, jittered)
        current *= phi

class RetrySupervisor:
    """A context-aware wrapper that executes callables with adaptive backoff."""

    def __init__(
        self,
        max_attempts: int = 4,
        base_delay: float = 0.5,
        max_delay: float = 5.0,
        exceptions: Sequence[Type[BaseException]] = (Exception,),
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exceptions = tuple(exceptions)

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = _golden_jitter_backoff(self.base_delay, self.max_delay)
            last_err = None

            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as err:
                    last_err = err
                    if attempt == self.max_attempts:
                        break
                    wait_time = next(delays)
                    time.sleep(wait_time)

            raise RuntimeError(
                f"Operation '{func.__name__}' failed after {self.max_attempts} attempts"
            ) from last_err

        return wrapper

def retry_network_op(
    max_attempts: int = 3,
    catch: Sequence[Type[BaseException]] = (ConnectionError, TimeoutError, OSError),
) -> Callable[..., Any]:
    """Convenience decorator specifically tuned for transient network glitches."""
    return RetrySupervisor(max_attempts=max_attempts, exceptions=catch)
