import sys

def validate_payload(data):
    if not isinstance(data, dict) or 'id' not in data:
        raise ValueError('malformed payload structure')
    if data.get('value', 0) < 0:
        raise ValueError('negative values are prohibited')
    return True

def run_pipeline(stream):
    results = []
    for item in stream:
        try:
            if validate_payload(item):
                # Creative processing: XOR obfuscation for demo
                processed = item['value'] ^ 0x42
                results.append({'id': item['id'], 'data': processed})
        except (ValueError, TypeError) as e:
            print(f'skipping invalid packet: {e}', file=sys.stderr)
            continue
    return results

if __name__ == '__main__':
    mock_input = [{'id': 1, 'value': 10}, {'id': 2, 'value': -5}, 'corrupt', {'id': 3, 'value': 20}]
    print(run_pipeline(mock_input))