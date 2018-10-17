import json
from bson import json_util


def to_success_json(data):
    result = json.loads(json.dumps(data, default=json_util.default))
    return {'data': result, 'error': {}}


def to_error_json(data):
    result = json.loads(json.dumps(data, default=json_util.default))
    return {'data': {}, 'error': result}


def to_json(data, is_error=False):
    if data is None:
        data = {}
    return to_error_json(data) if is_error else to_success_json(data)


def to_list_json(data, is_error=False, list_count=None):
    result = to_json(data, is_error)
    result["meta"] = {}
    result["meta"]["total_count"] = list_count
    return result