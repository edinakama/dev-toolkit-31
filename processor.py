import logging
from typing import Any, Generator, Dict, Type

logger = logging.getLogger("dev-toolkit-31")

class ProcessingError(ValueError):
    """Custom exception raised when payload validation fails."""
    pass

class StreamProcessor:
    """
    Processes a stream of raw payloads with runtime type coercion and validation.
    """
    def __init__(self, schema: Dict[str, Type]):
        self.schema = schema

    def validate_record(self, record: Any) -> Dict[str, Any]:
        if not isinstance(record, dict):
            raise ProcessingError(f"Expected dict input, got {type(record).__name__}")
        
        validated = {}
        for field, expected_type in self.schema.items():
            if field not in record:
                raise ProcessingError(f"Missing required field: '{field}'")
            
            value = record[field]
            if not isinstance(value, expected_type):
                try:
                    validated[field] = expected_type(value)
                except (ValueError, TypeError) as err:
                    raise ProcessingError(
                        f"Field '{field}' cannot be coerced to {expected_type.__name__}"
                    ) from err
            else:
                validated[field] = value
        return validated

    def execute(self, data_stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
        """
        Main processing loop enforcing structural checks on incoming streaming data.
        """
        for item in data_stream:
            try:
                if not item:
                    continue
                processed = self.validate_record(item)
                processed["_status"] = "verified"
                yield processed
            except ProcessingError as err:
                logger.warning(f"Skipping invalid item: {err}")
                yield {"_status": "rejected", "raw": item, "error": str(err)}
