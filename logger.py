import sys
import datetime
from functools import partial

class Logger:
    def __init__(self, prefix: str = 'DEV-TOOLKIT'):
        self.prefix = prefix
        self.stream = sys.stdout

    def __call__(self, level: str, message: str):
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f'[{ts}] {self.prefix.upper()} | {level.upper()} | {message}'
        print(entry, file=self.stream)

    @property
    def info(self):
        return partial(self, 'info')

    @property
    def warn(self):
        return partial(self, 'warn')

    @property
    def error(self):
        return partial(self, 'error')

    def reconfigure_stream(self, new_stream):
        self.stream = new_stream

def get_logger(name: str = 'root') -> Logger:
    return Logger(prefix=name)

if __name__ == '__main__':
    log = get_logger('dev-toolkit-31')
    log.info('initialization complete')
    log.warn('resource usage creeping upward')
    log.error('memory leak detected in sub-routine')