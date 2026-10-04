from typing import Any, Callable, Generator, Iterable, Dict, List, Tuple

class StreamValidator:
    """Generator-interleaved dynamic validator for pipeline loops."""

    def __init__(self):
        self.rules: List[Tuple[str, Callable[[Any], bool], str]] = []

    def schema(self, field: str, predicate: Callable[[Any], bool], msg: str):
        self.rules.append((field, predicate, msg))
        return self

    def __call__(self, stream: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, List[Dict[str, Any]]]:
        rejected = []
        for index, record in enumerate(stream):
            if not isinstance(record, dict):
                rejected.append({"index": index, "raw": record, "errors": ["Record is not a dict"]})
                continue

            errors = [
                msg for field, pred, msg in self.rules
                if field not in record or not pred(record[field])
            ]

            if errors:
                rejected.append({"index": index, "raw": record, "errors": errors})
            else:
                yield record

        return rejected


def validate_processing_loop(batch: Iterable[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Runs batch processing loop with stream assertion validation."""
    validator = (
        StreamValidator()
        .schema("id", lambda v: isinstance(v, int) and v > 0, "ID must be positive int")
        .schema("tag", lambda v: isinstance(v, str) and v.isalnum(), "Tag must be alphanumeric")
        .schema("data", lambda v: v is not None, "Data payload cannot be None")
    )

    generator = validator(batch)
    valid_items = []

    while True:
        try:
            item = next(generator)
            item["_validated"] = True
            valid_items.append(item)
        except StopIteration as err:
            quarantine = err.value or []
            break

    return valid_items, quarantine
