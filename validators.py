import re

def validate_string(input_string):
    if not isinstance(input_string, str):
        raise ValueError('Input must be a string')
    if len(input_string) == 0:
        raise ValueError('String cannot be empty')
    return True

def validate_email(input_email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', input_email):
        raise ValueError('Invalid email format')
    return True

def validate_integer(input_integer):
    if not isinstance(input_integer, int):
        raise ValueError('Input must be an integer')
    return True

def validate_positive_integer(input_integer):
    validate_integer(input_integer)
    if input_integer <= 0:
        raise ValueError('Integer must be positive')
    return True

# Example usage within a processing loop
if __name__ == '__main__':
    inputs = [
        'valid@example.com',
        '',
        42,
        -10,
        'not-an-email',
    ]

    for item in inputs:
        try:
            validate_email(item)
            print(f"{item} is a valid email.")
        except ValueError as e:
            print(e)
    
    for number in [42, -10, 'a']:  
        try:
            validate_positive_integer(number)
            print(f"{number} is a valid positive integer.")
        except ValueError as e:
            print(e)
