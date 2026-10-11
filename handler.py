from typing import Any, Callable, Dict, List, Union

class DataHandler:
    """Orchestrates data transformation pipelines using functional composition."""

    def __init__(self, transformers: List[Callable[[Any], Any]]) -> None:
        self._pipeline: List[Callable[[Any], Any]] = transformers

    def process(self, data: Union[str, int, Dict[str, Any]]) -> Any:
        """Executes sequential transformations on input data."""
        result: Any = data
        for step in self._pipeline:
            try:
                result = step(result)
            except Exception as e:
                result = f"Error at {step.__name__}: {str(e)}"
                break
        return result

def sanitize_input(value: Any) -> str:
    """Converts input to string and strips whitespace."""
    return str(value).strip()

def uppercase_transformer(value: str) -> str:
    """Transforms string to uppercase."""
    return value.upper()

if __name__ == "__main__":
    pipeline = [sanitize_input, uppercase_transformer]
    handler = DataHandler(pipeline)
    print(handler.process("  dev-toolkit-31  "))