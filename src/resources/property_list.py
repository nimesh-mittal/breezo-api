# ------------------------------------------------------------------------------
# FLASK FEATURES IMPORT
# ------------------------------------------------------------------------------
import datetime
import json
import uuid

import pytz
from flask import request
from flask_restful import Resource

from src.services.properties import PropertyService
from src.services.property_schema import property_schema, list_arg_schema
from src.commons.json_validator import validate_schema


class PropertyListResource(Resource):

    def __init__(self):
        db_name = 'breeze_db'
        self.store_service = PropertyService(db_name)

    @validate_schema(list_arg_schema(), is_arg=True)
    def get(self, service_id):
        limit = request.args.get("limit", 10)
        offset = request.args.get("offset", 0)
        keyword = request.args.get("keyword", "")
        properties = self.store_service.list_property(limit, offset, service_id, keyword)
        return properties

    @validate_schema(property_schema())
    def post(self, service_id):
        data = json.loads(request.data.decode('utf-8'))
        tz = pytz.timezone('Asia/Kolkata')
        data_ext = {
            'service_id': service_id,
            'field_id': str(uuid.uuid4()),
            'tenant': str(data['tenant']),
            'ip': str(data['ip']),
            'name': str(data['name']),
            'value': str(data['value']),
            'created_at': str(datetime.datetime.now(tz)),
            'created_by': str('unknown'),
            'updated_at': str(datetime.datetime.now(tz)),
            'updated_by': str('unknown')
        }

        property = self.store_service.create_property(data_ext)
        return property
