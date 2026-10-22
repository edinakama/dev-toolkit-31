import functools
from typing import Any, Callable, Dict, List

class DataProcessor:
    def __init__(self, pipeline: List[Callable] = None):
        self.pipeline = pipeline or []

    def add_step(self, func: Callable) -> None:
        self.pipeline.append(func)

    def execute(self, data: Any) -> Any:
        return functools.reduce(lambda acc, step: step(acc), self.pipeline, data)

    @staticmethod
    def sanitize(data: str) -> str:
        return data.strip().lower()

    @staticmethod
    def tag_context(data: Dict) -> Dict:
        return {**data, 'processed': True}

def process_stream(items: List[Dict]) -> List[Dict]:
    processor = DataProcessor([
        lambda d: {k: DataProcessor.sanitize(str(v)) if isinstance(v, str) else v for k, v in d.items()},
        DataProcessor.tag_context
    ])
    return [processor.execute(item) for item in items]

if __name__ == '__main__':
    raw_data = [{'name': '  DEV-TOOLKIT  ', 'id': 31}, {'name': '  PYTHON  ', 'id': 42}]
    print(process_stream(raw_data))