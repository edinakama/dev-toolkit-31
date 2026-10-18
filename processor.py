import sys
from typing import Any, Dict, Generator, List, Tuple


class ValidationError(Exception):
    """Raised when stream payload fails strict type or schema checks."""
    pass


def validate_payload(raw: Any) -> Dict[str, Any]:
    match raw:
        case {"action": str(act), "data": list(items)} if act in ("ingest", "purge") and items:
            cleaned = [x for x in items if isinstance(x, (int, float, str))]
            if not cleaned:
                raise ValidationError("Payload 'data' array contains no scalar values")
            return {"action": act, "data": cleaned}
        case {"action": "ping"}:
            return {"action": "pong", "data": []}
        case _:
            raise ValidationError(f"Malformed stream payload envelope: {raw!r}")


def data_stream_processor(inputs: List[Any]) -> Generator[Tuple[bool, Any], None, None]:
    """Main processing loop enforcing input validation via structural matching."""
    for index, raw_input in enumerate(inputs):
        try:
            if not isinstance(raw_input, dict):
                raise ValidationError(f"Expected record dict at index {index}, got {type(raw_input).__name__}")
            
            validated = validate_payload(raw_input)
            
            if validated["action"] == "ingest":
                result = f"Processed {len(validated['data'])} records"
            elif validated["action"] == "purge":
                result = f"Purged {len(validated['data'])} records"
            else:
                result = "Heartbeat acknowledged"
                
            yield (True, {"index": index, "status": "success", "result": result})
            
        except ValidationError as err:
            yield (False, {"index": index, "status": "rejected", "error": str(err)})


if __name__ == "__main__":
    sample_batch = [
        {"action": "ingest", "data": [10, 20, "valid"]},
        {"action": "invalid_cmd", "data": [1, 2]},
        "bad_string_element",
        {"action": "ping"},
        {"action": "purge", "data": []},
    ]

    for success, payload in data_stream_processor(sample_batch):
        label = "OK" if success else "ERR"
        msg = payload.get("result") or payload.get("error")
        print(f"[{label}] Frame {payload['index']}: {msg}")
