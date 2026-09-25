import re

class DataValidator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        for key, validator_func in self.schema.items():
            value = data.get(key)
            if not validator_func(value):
                raise ValueError(f"validation failed for key: {key} with value: {value}")
        return True

def is_alphanumeric(val):
    return isinstance(val, str) and val.isalnum()

def is_positive_int(val):
    return isinstance(val, int) and val > 0

def is_valid_email(val):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", str(val)))

# Schema definitions for the processor loop
PROCESSOR_SCHEMA = {
    "user_id": is_positive_int,
    "username": is_alphanumeric,
    "email": is_valid_email
}

def process_stream(data_stream):
    validator = DataValidator(PROCESSOR_SCHEMA)
    results = []
    for entry in data_stream:
        try:
            if validator.validate(entry):
                results.append({"status": "success", "data": entry})
        except ValueError as e:
            results.append({"status": "error", "message": str(e)})
    return results