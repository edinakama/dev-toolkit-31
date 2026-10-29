import re
import functools
from typing import Callable, Any, List, Dict, TypeVar

T = TypeVar('T')

class ProcessingPipeline:
    """A dynamic pipeline that automatically chains registered cleanup functions."""

    def __init__(self):
        self._steps: List[Dict[str, Any]] = []

    def register(self, priority: int = 10, name: str = None):
        """Decorator to register a processing step with priority ordering."""
        def decorator(func: Callable[[Any], Any]):
            step_name = name or func.__name__
            self._steps.append({'priority': priority, 'name': step_name, 'func': func})
            self._steps.sort(key=lambda s: s['priority'])
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def __call__(self, data: Any) -> Any:
        """Execute all organized steps sequentially on the input payload."""
        return functools.reduce(
            lambda val, step: step['func'](val),
            self._steps,
            data
        )

    @property
    def manifest(self) -> List[str]:
        return [s['name'] for s in self._steps]


pipeline = ProcessingPipeline()

@pipeline.register(priority=1, name="strip_whitespace")
def _clean_str(text: str) -> str:
    return text.strip() if isinstance(text, str) else text

@pipeline.register(priority=2, name="normalize_spaces")
def _squeeze_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text) if isinstance(text, str) else text

@pipeline.register(priority=3, name="sanitize_control_chars")
def _remove_control(text: str) -> str:
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text) if isinstance(text, str) else text

def process_data(payload: Any) -> Any:
    """Entry point for data reorganization and sanitization."""
    if isinstance(payload, dict):
        return {k: pipeline(v) for k, v in payload.items()}
    elif isinstance(payload, list):
        return [pipeline(item) for item in payload]
    return pipeline(payload)
