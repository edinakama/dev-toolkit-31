import sys
import time
from functools import lru_cache

class FastLogger:
    def __init__(self, level='INFO'):
        self.level = level
        self._cache = {}
        self._write = sys.stdout.write

    @lru_cache(maxsize=128)
    def _format_msg(self, msg):
        return f"[{time.strftime('%H:%M:%S')}] {msg}\n"

    def log(self, message):
        formatted = self._format_msg(message)
        self._write(formatted)

    def batch_log(self, messages):
        output = ''.join(map(self._format_msg, messages))
        self._write(output)

instance = FastLogger()

def log(msg):
    instance.log(msg)

def bulk(msgs):
    instance.batch_log(tuple(msgs))