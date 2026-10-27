import time
import threading
from collections import deque

class AsyncBufferLogger:
    def __init__(self, capacity=1000, flush_interval=5):
        self._buffer = deque(maxlen=capacity)
        self._interval = flush_interval
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._flusher, daemon=True)
        self._thread.start()

    def log(self, message):
        timestamp = time.time_ns()
        self._buffer.append(f'[{timestamp}] {message}')

    def _flusher(self):
        while not self._stop_event.is_set():
            time.sleep(self._interval)
            self._write_batch()

    def _write_batch(self):
        batch = list(self._buffer)
        if batch:
            with open('system.log', 'a') as f:
                f.write('\n'.join(batch) + '\n')
            for _ in range(len(batch)):
                try:
                    self._buffer.popleft()
                except IndexError:
                    break

    def shutdown(self):
        self._stop_event.set()
        self._write_batch()
        self._thread.join()