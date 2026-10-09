import collections
from typing import Any, Dict, Generator, List

class DynamicHandler:
    """Processes payload streams with a self-correcting dynamic validation step."""
    
    def __init__(self, strictly_typed: bool = True):
        self.strictly_typed = strictly_typed
        self.rejected_inputs: List[Dict[str, Any]] = []

    def _is_valid(self, payload: Any) -> bool:
        if not isinstance(payload, collections.abc.Mapping):
            return False
        
        if "id" not in payload or "action" not in payload:
            return False
            
        try:
            id_is_int = isinstance(payload["id"], int)
            action_is_clean = isinstance(payload["action"], str) and payload["action"].isalpha()
            return id_is_int and action_is_clean
        except (KeyError, AttributeError):
            return False

    def stream_processor(self, items: List[Any]) -> Generator[Dict[str, Any], None, None]:
        """Main loop utilizing yield-based generators and dynamic verification."""
        iterator = iter(items)
        while True:
            try:
                current_item = next(iterator)
            except StopIteration:
                break
            
            if self._is_valid(current_item):
                clean_item = dict(current_item)
                clean_item["processed"] = True
                yield clean_item
            else:
                self.rejected_inputs.append({
                    "original_item": current_item,
                    "class_type": type(current_item).__name__
                })
