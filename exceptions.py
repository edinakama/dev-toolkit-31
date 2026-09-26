from typing import Any, Optional

class DataProcessingError(Exception):
    """Base exception for dev-toolkit-31 data mutations."""
    def __init__(self, message: str, payload: Optional[Any] = None):
        super().__init__(message)
        self.payload = payload

def cast_with_resilience(target_type: type, value: Any, fallback: Any = None) -> Any:
    """An unorthodox casting engine using try-except flow control."""
    try:
        return target_type(value)
    except (ValueError, TypeError, AttributeError):
        if fallback is not None:
            return fallback
        raise DataProcessingError(
            f"Uncastable value: {value!r} to {target_type.__name__}", 
            payload=value
        )

class UnpackingError(DataProcessingError):
    """Specific trap for corrupted iterator patterns."""
    pass

def safe_unpack(data: Any, keys: list) -> dict:
    """Dict extraction with strict structural enforcement."""
    try:
        return {k: data[k] for k in keys}
    except (KeyError, TypeError) as e:
        raise UnpackingError(f"Structure mismatch: {e}", payload=data) from e