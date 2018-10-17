# ------------------------------------------------------------------------------
# FLASK FEATURES IMPORT
# ------------------------------------------------------------------------------
import datetime
import json
import uuid

import pytz
from flask import request
from flask_restful import Resource

from src.services.service_schema import service_schema, list_arg_schema
from src.services.services import ServiceService
from src.commons.json_validator import validate_schema


class ServiceListResource(Resource):

    def __init__(self):
        db_name = 'breeze_db'
        self.store_service = ServiceService(db_name)

    @validate_schema(list_arg_schema(), is_arg=True)
    def get(self):
        limit = request.args.get("limit", 10)
        offset = request.args.get("offset", 0)
        keyword = request.args.get("keyword", "")
        services = self.store_service.list_service(limit, offset, keyword)
        return services

    @validate_schema(service_schema())
    def post(self):
        data = json.loads(request.data.decode('utf-8'))
        tz = pytz.timezone('Asia/Kolkata')
        data_ext = {
            'service_id': str(uuid.uuid4()),
            'name': str(data['name']),
            'created_at': str(datetime.datetime.now(tz)),
            'created_by': str('unknown'),
            'updated_at': str(datetime.datetime.now(tz)),
            'updated_by': str('unknown')
        }

        service = self.store_service.create_service(data_ext)
        return service
