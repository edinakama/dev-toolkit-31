from typing import Callable, Any, Generator, Dict, List, Tuple

class ValidationError(Exception):
    def __init__(self, key: str, value: Any, rule_name: str):
        super().__init__(f"Validation failed for '{key}'={value!r} on rule '{rule_name}'")
        self.key, self.value, self.rule_name = key, value, rule_name

class StreamValidator:
    def __init__(self, **schema: Callable[[Any], bool]):
        self.schema = schema

    def __ror__(self, item: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(item, dict):
            raise ValidationError("root", type(item).__name__, "must_be_dict")
        for key, predicate in self.schema.items():
            if key not in item:
                raise ValidationError(key, None, "presence_check")
            if not predicate(item[key]):
                raise ValidationError(key, item[key], getattr(predicate, "__name__", "predicate"))
        return item

def process_batch(stream: List[Dict[str, Any]], validator: StreamValidator) -> Generator[Tuple[bool, Dict[str, Any]], None, None]:
    """Main processing loop using pipe-syntax input validation."""
    for index, raw_item in enumerate(stream):
        try:
            valid_item = raw_item | validator
            transformed = {k: v.strip().lower() if isinstance(v, str) else v for k, v in valid_item.items()}
            yield (True, {"seq": index, "payload": transformed})
        except ValidationError as err:
            yield (False, {"seq": index, "error": str(err), "raw": raw_item})

def is_positive_int(val: Any) -> bool:
    return isinstance(val, int) and val > 0

def is_nonempty_str(val: Any) -> bool:
    return isinstance(val, str) and bool(val.strip())

if __name__ == "__main__":
    validator = StreamValidator(id=is_positive_int, action=is_nonempty_str)
    batch = [
        {"id": 1, "action": "START\