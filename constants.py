from typing import Final, Dict, List, Any

# Configuration constants for dev-toolkit-31
# Using a mapping structure to store environment-specific thresholds

MAX_RETRIES: Final[int] = 5
TIMEOUT_SECONDS: Final[float] = 30.5

APP_CATEGORIES: Final[List[str]] = ['data', 'network', 'io', 'system']

def get_default_settings() -> Dict[str, Any]:
    """
    Retrieves the base configuration dictionary for the toolkit.

    Returns:
        Dict[str, Any]: A mapping containing default operational parameters.
    """
    return {
        "version": "3.1.0",
        "debug_mode": False,
        "buffer_size": 1024,
        "log_level": "INFO"
    }

class ToolStatus:
    """
    Represents the operational state constants for toolkit modules.
    """
    READY: Final[str] = "READY"
    BUSY: Final[str] = "BUSY"
    ERROR: Final[str] = "ERROR"
    IDLE: Final[str] = "IDLE"

def get_status_lookup() -> Dict[int, str]:
    """
    Maps internal integer codes to human-readable status strings.

    Returns:
        Dict[int, str]: An integer-indexed status mapping.
    """
    return {
        0: ToolStatus.IDLE,
        1: ToolStatus.READY,
        2: ToolStatus.BUSY,
        3: ToolStatus.ERROR
    }