from jsonschema import Draft4Validator
from functools import wraps
from flask import jsonify, request


class Prop:
    def __init__(self):
        self.field_type = "string"
        self.max_len = None
        self.min_len = None
        self._properties = {}
        self._items = {}
        self.enum_list = []

    def boolean(self):
        self.field_type = "boolean"
        return self

    def number(self):
        self.field_type = "number"
        return self

    def string(self):
        self.field_type = "string"
        return self

    def array(self):
        self.field_type = "array"
        return self

    def object(self):
        self.field_type = "object"
        return self

    def properties(self, schema):
        self._properties = schema
        return self

    def items(self, schema):
        self._items = schema
        return self

    def max(self, value):
        self.max_len = value
        return self

    def min(self, value):
        self.min_len = value
        return self

    def enum(self, value):
        self.enum_list = value
        return self

    def build(self):
        prop = {"type": self.field_type}

        if self.field_type == "object":
            prop["properties"] = self._properties

        if self.field_type == "array":
            prop["items"] = self._items

        if self.max_len is not None:
            prop["maxLength"] = self.max_len

        if self.min_len is not None:
            prop["minLength"] = self.min_len

        if len(self.enum_list) > 0:
            prop["enum"] = self.enum_list

        return prop


class Schema:

    def __init__(self):
        self.schema_type = "object"
        self.additionalProperties = False

    def keys(self, properties):
        self.keys = properties
        return self

    def required(self, fields):
        self.required = fields
        return self

    def additionalProperties(self, flag):
        self.additionalProperties = flag
        return self

    def build(self):
        return dict(type=self.schema_type, properties=self.keys, required=self.required, additionalProperties=self.additionalProperties)


def validate_schema(schema, is_arg=False, is_path=False):
    validator = Draft4Validator(schema)

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if(is_arg):
                input = request.args
            elif(is_path):
                input = request.view_args
            else:
                input = request.get_json(force=True)
            errors = [error.message for error in validator.iter_errors(input)]
            if errors:
                response = jsonify(dict(error=dict(code="X1028", message=errors), data=False))
                response.status_code = 406
                return response
            else:
                return fn(*args, **kwargs)
        return wrapped
    return wrapper