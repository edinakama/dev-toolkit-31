import re
from typing import Any, Callable, Dict, List

class InputGuardian:
    """Dynamic pipeline validator for dev-toolkit-31 stream processing."""
    def __init__(self):
        self._registry: Dict[str, List[Callable]] = {}

    def register(self, field: str, validator: Callable[[Any], bool]):
        if field not in self._registry:
            self._registry[field] = []
        self._registry[field].append(validator)

    def validate(self, payload: Dict[str, Any]) -> bool:
        for field, rules in self._registry.items():
            val = payload.get(field)
            if not all(rule(val) for rule in rules):
                return False
        return True

# Pre-defined creative validation rules
rules = {
    "non_empty": lambda x: bool(x and str(x).strip()),
    "is_alphanumeric": lambda x: bool(re.match(r'^[a-zA-Z0-9]+$', str(x)) if x else False),
    "min_length": lambda n: lambda x: len(str(x)) >= n
}

def get_validator_instance():
    guardian = InputGuardian()
    guardian.register("task_id", rules["is_alphanumeric"])
    guardian.register("payload", rules["non_empty"])
    return guardian

# Usage in processing loop:
# validator = get_validator_instance()
# if validator.validate(data): process(data)
# else: log_error("Malformed stream packet")