import functools
import itertools
from typing import Any, Callable, Dict, List

class DataPipeline:
    def __init__(self, processors: List[Callable[[Any], Any]]):
        self.pipeline = processors

    def execute(self, data: Any) -> Any:
        return functools.reduce(lambda acc, proc: proc(acc), self.pipeline, data)

class ProcessorRegistry:
    def __init__(self):
        self._registry: Dict[str, Callable] = {}

    def register(self, name: str):
        def decorator(func: Callable):
            self._registry[name] = func
            return func
        return decorator

    def get_chain(self, names: List[str]) -> List[Callable]:
        return [self._registry[n] for n in names if n in self._registry]

def sanitize(data: str) -> str:
    return data.strip().lower()

def tokenize(data: str) -> List[str]:
    return data.split(' ')

def filter_empty(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t]

def run_transformation(raw_data: str) -> List[str]:
    ops = [sanitize, tokenize, filter_empty]
    pipeline = DataPipeline(ops)
    return pipeline.execute(raw_data)

if __name__ == '__main__':
    result = run_transformation('  dev-toolkit-31  is  cool  ')
    print(f'Processed sequence: {result}')