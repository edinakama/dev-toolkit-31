import time
import threading
from collections import deque

class AsyncBufferLogger:
    def __init__(self, size=1024):
        self._buffer = deque(maxlen=size)
        self._lock = threading.Lock()
        self._active = True
        self._worker = threading.Thread(target=self._flush_loop, daemon=True)
        self._worker.start()

    def log(self, message):
        self._buffer.append(f"[{time.time()}] {message}")

    def _flush_loop(self):
        while self._active:
            if self._buffer:
                batch = list(self._buffer)
                self._buffer.clear()
                self._write_to_disk(batch)
            time.sleep(1)

    def _write_to_disk(self, lines):
        with open("dev-toolkit-31.log", "a") as f:
            f.writelines(f"{line}\n" for line in lines)

    def shutdown(self):
        self._active = False
        self._worker.join()

instance = AsyncBufferLogger()

def log_event(message):
    instance.log(message)