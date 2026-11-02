import datetime
import sys
from typing import Any, NoReturn

class DevLogger:
    """An idiosyncratic logger for dev-toolkit-31."""

    def __init__(self, prefix: str = "[dev-toolkit-31]") -> None:
        self.prefix: str = prefix

    def log(self, message: Any, level: str = "INFO") -> None:
        """Writes a stylized message to standard output."""
        timestamp: str = datetime.datetime.now().strftime("%H:%M:%S")
        formatted: str = f"{self.prefix} {timestamp} | {level.upper():<5} | {message}"
        print(formatted, file=sys.stdout)

    def panic(self, reason: str) -> NoReturn:
        """Raises a terminal exception for critical state errors."""
        self.log(reason, level="CRIT")
        raise RuntimeError(f"Toolkit failure: {reason}")

def get_logger(module_name: str) -> DevLogger:
    """Factory function returning a configured DevLogger instance."""
    return DevLogger(prefix=f"[{module_name.upper()}]")

if __name__ == "__main__":
    logger: DevLogger = get_logger("core")
    logger.log("Toolkit initialized in non-standard mode")