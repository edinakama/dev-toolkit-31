import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

class DevToolkitLogger:
    def __init__(self, name='dev-toolkit-31', log_dir='logs'):
        self.path = Path(log_dir)
        self.path.mkdir(exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._configure()

    def _configure(self):
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )
        
        # Rotating file handler: 1MB per file, 5 backup files
        file_handler = RotatingFileHandler(
            self.path / 'app.log',
            maxBytes=1024*1024,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

logger = DevToolkitLogger().get_logger()