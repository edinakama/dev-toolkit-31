import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str, log_file: str = 'app.log') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # using a decorator-like approach to inject handler attributes
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # console fallback for non-production environments
        if os.getenv('DEV_MODE') == '1':
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
            
    return logger

# usage: log = get_logger(__name__)