import re

class DataSanitizer:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, payload):
        validated = {}
        for key, rules in self.schema.items():
            val = payload.get(key)
            if 'regex' in rules and not re.match(rules['regex'], str(val)):
                raise ValueError(f"Invalid format for field: {key}")
            if 'min_len' in rules and len(str(val)) < rules['min_len']:
                raise ValueError(f"Field {key} too short")
            validated[key] = val
        return validated

def main_loop(data_stream, schema):
    validator = DataSanitizer(schema)
    processed = []
    for entry in data_stream:
        try:
            clean = validator.validate(entry)
            processed.append(clean)
        except (ValueError, TypeError) as e:
            print(f"Skipping invalid entry: {e}")
            continue
    return processed

SCHEMA = {
    'username': {'regex': r'^[a-zA-Z0-9_]+$', 'min_len': 3},
    'port': {'regex': r'^\d+$'}
}