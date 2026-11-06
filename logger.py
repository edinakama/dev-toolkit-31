import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union

class CreativeRotator(RotatingFileHandler):
    """Custom rotating handler that inserts session banners upon log rotation."""
    def doRollover(self) -> None:
        super().doRollover()
        if self.stream:
            banner = f"\n{'=' * 40}\n--- LOG ROTATED: NEW SESSION STARTED ---\n{'=' * 40}\n"
            self.stream.write(banner)
            self.stream.flush()

def setup_logger(
    name: str = "dev_toolkit",
    log_dir: Union[str, Path] = "logs",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    """Configures a logger with custom size-based file rotation and console output."""
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    log_path = path / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="[%(asctime)s] | %(levelname)-7s | %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = CreativeRotator(
        filename=log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
