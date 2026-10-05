import re
from typing import Any, Dict, List, Union

class DeepDataDriller:
    """
    An extractor supporting dotted paths, index lookup, and wildcard mappings.
    """
    def __init__(self, data: Union[Dict, List]):
        self.data = data

    def drill(self, path: str, default: Any = None) -> Any:
        # Splitting on dots and bracket characters
        tokens = [t for t in re.split(r'\.|\[|\]', path) if t]
        return self._resolve(self.data, tokens, default)

    def _resolve(self, current: Any, tokens: List[str], default: Any) -> Any:
        if not tokens:
            return current

        head, tail = tokens[0], tokens[1:]

        if head == '*':
            if isinstance(current, list):
                results = []
                for item in current:
                    val = self._resolve(item, tail, default)
                    if val is not default:
                        results.append(val)
                return results if results else default
            return default

        if isinstance(current, dict):
            if head in current:
                return self._resolve(current[head], tail, default)
            # Fallback for dicts with integer keys
            try:
                int_key = int(head)
                if int_key in current:
                    return self._resolve(current[int_key], tail, default)
            except ValueError:
                pass
        elif isinstance(current, list):
            try:
                idx = int(head)
                if -len(current) <= idx < len(current):
                    return self._resolve(current[idx], tail, default)
            except ValueError:
                pass

        return default

def extract(data: Union[Dict, List], path: str, default: Any = None) -> Any:
    """Extract nested structures safely using dynamic dotted and wildcard syntax."""
    return DeepDataDriller(data).drill(path, default)