import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def merge_dictionaries(dict1, dict2):
    result = dict1.copy()
    result.update(dict2)
    return result


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def chunk_list(data_list, chunk_size):
    return [data_list[i:i + chunk_size] for i in range(0, len(data_list), chunk_size)]


def get_keys_from_dict(dictionary, keys):
    return {key: dictionary[key] for key in keys if key in dictionary}


def generate_unique_id(prefix='id_'):
    import uuid
    return f'{prefix}{uuid.uuid4()}'