from typing import Any, Callable, Dict, List, Optional

class InputGuardian:
    """Curated validation strategies for input streams."""
    def __init__(self):
        self._registry: Dict[str, List[Callable]] = {}

    def register(self, field: str, check: Callable[[Any], bool]) -> None:
        if field not in self._registry:
            self._registry[field] = []
        self._registry[field].append(check)

    def sanitize(self, data: Dict[str, Any]) -> bool:
        for key, value in data.items():
            validators = self._registry.get(key, [])
            if not all(func(value) for func in validators):
                return False
        return True

    @staticmethod
    def non_empty(val: Any) -> bool:
        return bool(val) and len(str(val).strip()) > 0

    @staticmethod
    def bounds(min_val: int, max_val: int) -> Callable:
        return lambda x: isinstance(x, (int, float)) and min_val <= x <= max_val

def execute_processing(data_stream: List[Dict[str, Any]]) -> None:
    guardian = InputGuardian()
    guardian.register("id", lambda x: isinstance(x, int))
    guardian.register("payload", InputGuardian.non_empty)
    guardian.register("level", InputGuardian.bounds(1, 10))

    for entry in data_stream:
        if guardian.sanitize(entry):
            print(f"Processing secure item: {entry.get('id')}")
        else:
            print(f"Dropped invalid entry: {entry}")