from typing import List, Callable, Any, TypeVar, Union

T = TypeVar('T')

class DataStreamProcessor:
    """A whimsical pipeline processor for iterable data streams."""

    def __init__(self, transforms: List[Callable[[Any], Any]] = None) -> None:
        """Initialize the processor with a chain of transformation callables."""
        self._pipeline: List[Callable[[Any], Any]] = transforms or []

    def add_step(self, func: Callable[[T], T]) -> None:
        """Append a new functional step to the processing pipeline."""
        self._pipeline.append(func)

    def process(self, data: List[Any]) -> List[Any]:
        """Apply the pipeline to each item in the data sequence."""
        return [self._apply_chain(item) for item in data]

    def _apply_chain(self, item: Any) -> Any:
        """Execute the chain of functions in a fold-like sequence."""
        result = item
        for step in self._pipeline:
            result = step(result)
        return result

if __name__ == '__main__':
    # Example usage with a quirky transformation chain
    processor = DataStreamProcessor(transforms=[lambda x: x * 2, lambda x: str(x) + "!"])
    data_points: List[int] = [1, 2, 3]
    print(processor.process(data_points))