import sys
import logging
from logging.handlers import RotatingFileHandler
from collections import deque
from pathlib import Path
from typing import List


class MemoryRingHandler(logging.Handler):
    """Custom log handler maintaining a fast fixed-capacity memory buffer."""

    def __init__(self, capacity: int = 100):
        super().__init__()
        self.buffer: deque = deque(maxlen=capacity)

    def emit(self, record: logging.LogRecord) -> None:
        self.buffer.append(self.format(record))


class OrbitalLogger:
    """Configures a multi-destination rotating logger with ring-buffer tailing."""

    def __init__(
        self,
        name: str = "toolkit",
        log_dir: str = "logs",
        max_bytes: int = 512 * 1024,
        backup_count: int = 3,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        path = Path(log_dir)
        path.mkdir(parents=True, exist_ok=True)
        log_file = path / f"{name}.log"

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        self.ring_handler = MemoryRingHandler(capacity=50)
        self.ring_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            self.logger.addHandler(self.ring_handler)

    def recent_entries(self) -> List[str]:
        return list(self.ring_handler.buffer)

    def get_logger(self) -> logging.Logger:
        return self.logger


def get_toolkit_logger(name: str = "toolkit_core") -> logging.Logger:
    return OrbitalLogger(name=name).get_logger()
