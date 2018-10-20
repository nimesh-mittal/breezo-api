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


class ServiceNameResource(Resource):

    def __init__(self):
        db_name = 'breeze_db'
        self.service = ServiceService(db_name)

    @validate_schema(id_path_schema(), is_path=True)
    def get(self, service_name):
        service = self.service.get_service_by_name(service_name)
        return service
