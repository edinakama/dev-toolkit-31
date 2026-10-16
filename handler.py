import sys
import traceback
import logging

class OperationalFault(Exception):
    pass

def robust_execution(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logging.error(f'Edge case caught: {type(e).__name__} -> {e}')
            return None
        except Exception as e:
            logging.critical(f'Unexpected systemic failure: {traceback.format_exc()}')
            raise OperationalFault('System state compromised') from e
    return wrapper

@robust_execution
def process_data(payload):
    if not isinstance(payload, dict):
        raise TypeError('Input must be a dictionary')
    return {k: v * 2 for k, v in payload.items()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    data = {'val': 10, 'empty': 0}
    result = process_data(data)
    print(f'Processed: {result}')
    failure = process_data('invalid_type')
    print(f'Safe return on failure: {failure}')