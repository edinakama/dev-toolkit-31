import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_dev_logger(name: str = 'dev-toolkit-31', log_file: str = 'app.log') -> logging.Logger:
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Creative rotating handler with specific limits
        handler = RotatingFileHandler(
            path,
            maxBytes=1024 * 1024 * 5,
            backupCount=3,
            encoding='utf-8'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Console stream as secondary auditor
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

if __name__ == '__main__':
    log = get_dev_logger()
    log.info('toolkit initialized with rotation logic')