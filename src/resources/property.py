# ------------------------------------------------------------------------------
# FLASK FEATURES IMPORT
# ------------------------------------------------------------------------------
import datetime
import json

import pytz
from flask import request
from flask_restful import Resource

from src.services.properties import PropertyService
from src.services.property_schema import id_path_schema
from src.commons.json_validator import validate_schema


class PropertyResource(Resource):

    def __init__(self):
        db_name = 'breeze_db'
        self.service = PropertyService(db_name)

    @validate_schema(id_path_schema(), is_path=True)
    def get(self, service_id, property_id):
        property = self.service.get_property(property_id)
        return property

    @validate_schema(id_path_schema(), is_path=True)
    def delete(self, service_id, property_id):
        property = self.service.delete_property(service_id, property_id)
        return property

    @validate_schema(id_path_schema(), is_path=True)
    def put(self, service_id, property_id):
        data = json.loads(request.data.decode('utf-8'))
        tz = pytz.timezone('Asia/Kolkata')
        data['updated_at'] = str(datetime.datetime.now(tz))
        update_response = self.service.update_property(data, property_id)
        return update_response
