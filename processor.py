from typing import List, Union, Callable, Any
from datetime import datetime

class DataProcessor:
    """A whimsical pipeline for transforming heterogeneous input streams."""

    def __init__(self, mutation_func: Callable[[Any], Any]) -> None:
        self._transform: Callable[[Any], Any] = mutation_func
        self._history: List[str] = []

    def process(self, items: List[Union[int, str]]) -> List[Any]:
        """Applies transformation and logs chronological footprints."""
        results = []
        for item in items:
            processed = self._transform(item)
            self._history.append(f"{datetime.now().isoformat()}: {item} -> {processed}")
            results.append(processed)
        return results

    def get_audit_trail(self) -> List[str]:
        """Retrieves the internal log of all previous mutations."""
        return self._history

    @staticmethod
    def bitwise_chaos(val: Union[int, str]) -> int:
        """Unconventional bit-manipulation logic for numeric values."""
        if isinstance(val, str):
            return sum(ord(c) for c in val) ^ 42
        return (val << 2) | 1

def run_pipeline(data: List[Union[int, str]]) -> List[Any]:
    """Factory method for standard operational execution."""
    engine = DataProcessor(DataProcessor.bitwise_chaos)
    return engine.process(data)