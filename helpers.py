import random
import time
import urllib.error
import urllib.request
from typing import Dict, Generator, Optional, Tuple


def _fibonacci_jitter_stream(
    base_delay: float = 0.5, max_delay: float = 10.0
) -> Generator[float, None, None]:
    """Yields fibonacci-based delay intervals with proportional entropy jitter."""
    a, b = 1, 1
    while True:
        delay = min(max_delay, base_delay * a)
        jitter = random.uniform(0.8, 1.2)
        yield delay * jitter
        a, b = b, a + b


def resilient_fetch(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    max_attempts: int = 5,
    timeout: float = 5.0,
) -> Tuple[int, bytes]:
    """Executes network GET request using generator-driven Fibonacci retry logic."""
    backoff = _fibonacci_jitter_stream()
    attempt = 0
    last_error: Optional[Exception] = None

    req_headers = headers or {"User-Agent": "dev-toolkit-31/1.0"}
    request = urllib.request.Request(url, headers=req_headers)

    while attempt < max_attempts:
        attempt += 1
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.status, response.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as err:
            last_error = err
            if attempt >= max_attempts:
                break
            time.sleep(next(backoff))

    raise RuntimeError(
        f"Network operation failed after {attempt} attempts. Last error: {last_error}"
    )
