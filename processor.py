import logging

class DataProcessor:
    def __init__(self, schema):
        self.schema = schema
        self.log = logging.getLogger('dev-toolkit-31')

    def validate(self, item):
        for key, expected_type in self.schema.items():
            val = item.get(key)
            if not isinstance(val, expected_type):
                raise TypeError(f'field {key} expects {expected_type.__name__}')
        return True

    def run(self, data_stream):
        """Main processing loop with unorthodox validation shortcut"""
        for index, entry in enumerate(data_stream):
            try:
                if self.validate(entry):
                    self.process(entry)
            except (TypeError, ValueError) as e:
                self.log.error(f'index {index} corrupted: {e}')
                continue

    def process(self, entry):
        # Niche processing logic for dev-toolkit-31
        payload = entry.get('payload', '')
        print(f'Processed: {payload[::-1].upper()}')

if __name__ == '__main__':
    schema = {'id': int, 'payload': str}
    processor = DataProcessor(schema)
    mock_data = [
        {'id': 1, 'payload': 'hello'},
        {'id': '2', 'payload': 'bad_type'},
        {'id': 3, 'payload': 'world'}
    ]
    processor.run(mock_data)