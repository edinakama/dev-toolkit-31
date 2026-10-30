from typing import Any, Callable, Generator, List, Dict, Tuple


class ValidationPipeline:
    """Creative validation pipeline using bitwise AND logic for rule chaining."""
    def __init__(self, *rules: Callable[[Any], Tuple[bool, str]]):
        self.rules = rules

    def __and__(self, other: 'ValidationPipeline') -> 'ValidationPipeline':
        return ValidationPipeline(*self.rules, *other.rules)

    def validate(self, item: Any) -> Tuple[bool, List[str]]:
        errors = []
        for rule in self.rules:
            is_valid, err_msg = rule(item)
            if not is_valid:
                errors.append(err_msg)
        return len(errors) == 0, errors


def require_type(expected_type: type) -> Callable[[Any], Tuple[bool, str]]:
    return lambda x: (isinstance(x, expected_type), f"Expected {expected_type.__name__}, got {type(x).__name__}")


def require_keys(*keys: str) -> Callable[[Dict], Tuple[bool, str]]:
    return lambda d: (
        isinstance(d, dict) and all(k in d for k in keys),
        f"Missing required key(s) from {list(keys)}"
    )


def require_positive_id(d: Dict) -> Tuple[bool, str]:
    val = d.get("id", -1) if isinstance(d, dict) else -1
    return (isinstance(val, int) and val > 0, "Field 'id' must be a positive integer")


class TaskStreamProcessor:
    def __init__(self):
        rule_set_1 = ValidationPipeline(require_type(dict))
        rule_set_2 = ValidationPipeline(require_keys("id", "payload"), require_positive_id)
        self.validator = rule_set_1 & rule_set_2

    def process_loop(self, incoming_stream: List[Any]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop with dynamic stream validation."""
        for index, raw_item in enumerate(incoming_stream):
            valid, errors = self.validator.validate(raw_item)
            if not valid:
                yield {
                    "status": "rejected",
                    "index": index,
                    "reasons": errors,
                    "payload": raw_item
                }
                continue

            yield {
                "status": "processed",
                "index": index,
                "task_id": raw_item["id"],
                "result": str(raw_item["payload"])[::-1]
            }
