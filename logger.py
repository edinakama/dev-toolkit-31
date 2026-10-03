import sys
import time
from typing import Any, Callable, TextIO, Union

class ChromaticLogger:
    """A colorful stream logger with dynamic severity tinting and execution timing.
    
    Transforms plain log payloads into color-coded, timestamped terminal output
    using ANSI escape sequences and custom formatting pipelines.
    """

    PALETTE: dict[str, str] = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARN": "\033[33m",
        "ERROR": "\033[31m",
        "RESET": "\033[0m",
    }

    def __init__(self, stream: TextIO = sys.stdout, show_time: bool = True) -> None:
        self.stream: TextIO = stream
        self.show_time: bool = show_time

    def _paint(self, level: str, message: str) -> str:
        color: str = self.PALETTE.get(level.upper(), self.PALETTE["RESET"])
        reset: str = self.PALETTE["RESET"]
        stamp: str = f"[{time.strftime('%H:%M:%S')}] " if self.show_time else ""
        return f"{color}{stamp}[{level.upper()}] {message}{reset}\n"

    def emit(self, level: str, payload: Union[str, Exception, Any]) -> int:
        """Writes formatted color output to the configured text stream.

        Args:
            level: Severity tag determining the ANSI palette color.
            payload: Raw object or error to stringify and log.

        Returns:
            Count of characters written to the target stream.
        """
        formatted: str = self._paint(level, str(payload))
        written: int = self.stream.write(formatted)
        self.stream.flush()
        return written

    def trace_execution(self, level: str = "INFO") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator that logs entry, exit, and runtime duration of functions."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                start: float = time.perf_counter()
                self.emit(level, f"Entering '{func.__name__}'")
                try:
                    result: Any = func(*args, **kwargs)
                    elapsed: float = (time.perf_counter() - start) * 1000
                    self.emit(level, f"Exited '{func.__name__}' in {elapsed:.2f}ms")
                    return result
                except Exception as err:
                    self.emit("ERROR", f"Failed '{func.__name__}': {err}")
                    raise
            return wrapper
        return decorator