import logging

def validate_payload(data):
    required = {'id': int, 'action': str}
    if not all(k in data and isinstance(data[k], v) for k, v in required.items()):
        raise ValueError('Schema mismatch detected')
    return True

def process_stream(stream):
    for entry in stream:
        try:
            if validate_payload(entry):
                print(f'Processing {entry["id"]}: {entry["action"]}')
        except (ValueError, TypeError) as e:
            logging.error(f'Skipping malformed packet: {e}')

if __name__ == '__main__':
    data_stream = [
        {'id': 1, 'action': 'sync'},
        {'id': 'fail', 'action': 'bad_type'},
        {'id': 2, 'action': 'backup'}
    ]
    process_stream(data_stream)