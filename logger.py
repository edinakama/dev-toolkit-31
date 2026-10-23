import datetime
import json
import sys
from typing import Any

class DataLogger:
    def __init__(self, target_stream=sys.stdout):
        self.stream = target_stream

    def __call__(self, data: Any, label: str = "INFO") -> None:
        self._log(data, label)

    def _log(self, data: Any, label: str) -> None:
        payload = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "label": label.upper(),
            "content": self._serialize(data)
        }
        print(json.dumps(payload), file=self.stream)

    def _serialize(self, data: Any) -> Any:
        try:
            return json.loads(json.dumps(data, default=str))
        except (TypeError, ValueError):
            return f"[UNSERIALIZABLE: {type(data).__name__}]"

def get_logger(stream=sys.stdout) -> DataLogger:
    return DataLogger(stream)

log = get_logger()

if __name__ == "__main__":
    log({"test": "data", "val": 42}, label="debug")