from src.commons.mongo_db import db_client
from src.commons.json_utils import to_json, to_list_json
from flask import g


class ServiceService:

    def __init__(self, db_name):
        self.db_name = db_name
        self.client = db_client

    def search_query(self, keyword):
        return {"$or":[{'name': {'$regex': keyword}}, {'description': {'$regex': keyword}}]}

    def find_query(self, client_id, app_id, query):
        if query is None:
            return {"$and":[{'client_id': client_id}, {'app_id': app_id}]}
        return {"$and":[{'client_id': client_id}, {'app_id': app_id}, query]}

    def list_service(self, limit, offset, keyword):
        query = self.search_query(keyword)
        result, count = self.client.find(self.db_name, "services", query=query, offset=offset, limit=limit)

        output = []
        for service in result:
            del service['_id']
            output.append(service)

        return to_list_json(output, list_count=count)

    def get_service(self, id):
        output, count =self.client.find(self.db_name, "services", {'ds_id': id})
        result = {}
        for service in output:
            result = service
            del result['_id']
        return to_json(result)

    def update_service(self, newObj, id):
        output = self.client.find_one_and_update(self.db_name, "services", {'ds_id': id}, {'$set':newObj})
        del output['_id']
        return to_json(output)

    def delete_service(self, id):
        result = self.client.find_one_and_delete(self.db_name, "services", {'service_id': id})
        return to_json(result)

    def delete_services(self, ids):
        results = []
        for id in ids:
            result = self.client.find_one_and_delete(self.db_name, "services", {'ds_id': id})
            results.append(result)
        return results

    def create_service(self, app):
        id = self.client.insert_one(self.db_name, "services", app).inserted_id
        del  app['_id']
        return to_json(app)