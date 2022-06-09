import json


def read_json(path):
    with open(f'{path}', "r") as json_data:
        json_read = json.load(json_data)

    return json_read


def write_json(path, object):
    with open(f'{path}', 'w') as json_data:
        json.dump(object, json_data)
