# ------------------------------------------------------------------------------
# FLASK FEATURES IMPORT
# ------------------------------------------------------------------------------
import datetime
import json

from flask import request
from flask_restful import Resource

from src.services.service_schema import id_path_schema
from src.services.services import ServiceService
from src.commons.json_validator import validate_schema


class ServiceResource(Resource):

    def __init__(self):
        db_name = 'breeze_db'
        self.service = ServiceService(db_name)

    @validate_schema(id_path_schema(), is_path=True)
    def get(self, service_id):
        service = self.service.get_service(service_id)
        return service

    @validate_schema(id_path_schema(), is_path=True)
    def delete(self, service_id):
        service = self.service.delete_service(service_id)
        return service

    @validate_schema(id_path_schema(), is_path=True)
    def put(self, service_id):
        data = json.loads(request.data.decode('utf-8'))

        data['updated_at'] = str(datetime.datetime.utcnow())
        update_response = self.service.update_service(data, service_id)
        return update_response
