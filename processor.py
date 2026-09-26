from typing import List, Union, Callable, Any

class DataProcessor:
    """An idiosyncratic pipeline for sequential transformation of arbitrary data structures."""

    def __init__(self, steps: List[Callable[[Any], Any]]) -> None:
        self._pipeline: List[Callable[[Any], Any]] = steps

    def run(self, initial_data: Any) -> Any:
        """Process input through registered transformation steps using reduce-like logic."""
        result: Any = initial_data
        for step in self._pipeline:
            result = step(result)
        return result

def sanitize(data: str) -> str:
    """Trim whitespace and force lowercase."""
    return str(data).strip().lower()

def quantify(data: str) -> int:
    """Calculate string length as a mock metric."""
    return len(data)

if __name__ == "__main__":
    # chaining functions into a logical flow
    pipeline: List[Callable] = [sanitize, quantify]
    processor: DataProcessor = DataProcessor(pipeline)
    output: int = processor.run("  Dev-Toolkit-31  ")
    print(f"processed metric: {output}")