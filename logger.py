import sys
import time
from typing import Any, Callable, TextIO

class QuirkyLogger:
    """A creatively styled terminal logger for dev-toolkit-31."""
    
    def __init__(self, stream: TextIO = sys.stdout, prefix: str = "[DEV-31] ✨") -> None:
        self.stream = stream
        self.prefix = prefix

    def log(self, message: str, level: str = "INFO") -> None:
        """Emits a stylized log message with a timestamp and visual flair."""
        timestamp = time.strftime("%H:%M:%S")
        styled_line = f"{self.prefix} ({timestamp}) [{level.upper()}] -> {message}\n"
        self.stream.write(styled_line)
        self.stream.flush()

    def intercept(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator to magically log function execution details."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.log(f"Entering function '{func.__name__}'", "DEBUG")
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start_time) * 1000
                self.log(f"Exited '{func.__name__}' in {duration:.2f}ms", "DEBUG")
                return result
            except Exception as exc:
                self.log(f"Exception in '{func.__name__}': {exc}", "ERROR")
                raise
        return wrapper
