import sys
import os
from typing import Any

class FaultTolerantLogger:
    """Resilient logger handling stream crashes, recursion, and unstr-able objects."""

    def __init__(self, primary_stream=sys.stdout, max_fallback_depth: int = 3):
        self.primary_stream = primary_stream
        self.max_fallback_depth = max_fallback_depth
        self._guard_flag = False

    def _safe_serialize(self, record: Any) -> str:
        try:
            return str(record)
        except Exception as err:
            try:
                return f"<Unprintable object {type(record).__name__}: {repr(err)}>"
            except Exception:
                return "<Unprintable object: stringification failed>"

    def log(self, message: Any, level: str = "INFO", depth: int = 0) -> bool:
        if depth > self.max_fallback_depth:
            return False

        if self._guard_flag and depth == 0:
            sys.stderr.write("[CRITICAL] Recursive logging call intercepted.\n")
            return False

        self._guard_flag = True
        try:
            formatted_msg = self._safe_serialize(message)
            out_str = f"[{level.upper()}] {formatted_msg}\n"
            
            try:
                self.primary_stream.write(out_str)
                self.primary_stream.flush()
                return True
            except (IOError, OSError, AttributeError):
                sys.stderr.write(f"[FALLBACK] {out_str}")
                sys.stderr.flush()
                return True
        except Exception as exc:
            try:
                err_msg = f"[EMERGENCY-LOG] {exc.__class__.__name__}\n".encode("utf-8")
                os.write(2, err_msg)
                return self.log(f"Recovered logging error: {exc}", level="ERROR", depth=depth + 1)
            except Exception:
                return False
        finally:
            self._guard_flag = False

def get_logger(stream=None) -> FaultTolerantLogger:
    return FaultTolerantLogger(primary_stream=stream or sys.stdout)
