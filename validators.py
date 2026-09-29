import math
from typing import Any, Generator, Tuple, Union


class ValidationFailure(ValueError):
    def __init__(self, path: tuple, message: str):
        self.path = path
        self.message = message
        super().__init__(f"At field '{'.'.join(map(str, path))}': {message}")


def coerce_quirky_boolean(val: Any) -> bool:
    if isinstance(val, str):
        norm = val.strip().lower()
        if norm in ('y', 'yes', 'true', '1', 'on', 'enable'):
            return True
        if norm in ('n', 'no', 'false', '0', 'off', 'disable'):
            return False
    if isinstance(val, (int, float)):
        return bool(val)
    raise ValueError(f"uncoercible boolean value: {val}")


def coerce_resilient_float(val: Any) -> float:
    if isinstance(val, str):
        clean = val.strip()
        if clean.endswith('%'):
            return float(clean[:-1]) / 100.0
    f_val = float(val)
    if math.isnan(f_val) or math.isinf(f_val):
        raise ValueError('infinity and nan are restricted in strict mode')
    return f_val


class DynamicValidator:
    def __init__(self, blueprint: dict):
        self.blueprint = blueprint

    def scrutinize(self, payload: dict) -> Tuple[dict, list[ValidationFailure]]:
        cleaned = {}
        failures = []
        if not isinstance(payload, dict):
            return cleaned, [ValidationFailure((), 'root element must be a dictionary')]

        for key, coercer in self.blueprint.items():
            path = (key,)
            if key not in payload:
                failures.append(ValidationFailure(path, 'missing mandatory key'))
                continue
            try:
                cleaned[key] = coercer(payload[key])
            except Exception as exc:
                failures.append(ValidationFailure(path, str(exc)))
        return cleaned, failures
