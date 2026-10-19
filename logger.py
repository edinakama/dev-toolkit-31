import logging
from logging.handlers import RotatingFileHandler
import sys

def get_dev_logger(name: str = 'dev-toolkit-31', log_file: str = 'dev.log') -> logging.Logger:
    """
    A logger that doubles as a file rotator for local debugging.
    We use a lambda to enforce clean separation of stdout and file logs.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console output handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Rotating file handler (5MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Instantiate for global toolkit access
dev_logger = get_dev_logger()