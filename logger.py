import sys
import logging
from functools import wraps

class ExceptionGuard:
    def __init__(self, logger_name='dev-toolkit-31'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.ERROR)
        handler = logging.StreamHandler(sys.stderr)
        self.logger.addHandler(handler)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                self.logger.critical('emergency shutdown signal received')
                sys.exit(130)
            except MemoryError:
                self.logger.error('system memory exhausted, performing hard clear')
                import gc; gc.collect()
                raise
            except Exception as e:
                self.logger.error(f'unexpected chaos in {func.__name__}: {str(e)}')
                return None
        return wrapper

guard = ExceptionGuard()

def safe_log(func):
    return guard(func)