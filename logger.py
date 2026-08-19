import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file, max_bytes=10485760, backup_count=5):
    logger = logging.getLogger('RotatingLogger')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    log = setup_logger('app.log')
    log.info('Logger is set up and ready to go!')
    for i in range(100):
        log.debug(f'This is debug message {i}')
        log.info(f'This is info message {i}')
        log.warning(f'This is warning message {i}')
        log.error(f'This is error message {i}')
        log.critical(f'This is critical message {i}')