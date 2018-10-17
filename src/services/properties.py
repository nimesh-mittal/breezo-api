from src.commons.mongo_db import db_client
from src.commons.json_utils import to_json, to_list_json
from pymongo import DESCENDING


class PropertyService:

    def __init__(self, db_name):
        self.db_name = db_name
        self.client = db_client

    def search_query(self, keyword):
        return {"$or":[{'name': {'$regex': keyword}}, {'value': {'$regex': keyword}}, {'tenant': {'$regex': keyword}}, {'ip': {'$regex': keyword}}]}

    def find_query(self, service_id, query):
        return {"$and":[{'service_id': service_id}, query]}

    def list_property(self, limit, offset, service_id, keyword):
        query = self.find_query(service_id, self.search_query(keyword))
        result, count = self.client.find(self.db_name, "properties", query=query, offset=offset, limit=limit, sort_field='updated_at', sort_order=DESCENDING)

        output = []
        for property in result:
            del property['_id']
            output.append(property)

        return to_list_json(output, list_count=count)

    def get_property(self, id):
        output, count =self.client.find(self.db_name, "properties", {'field_id': id})
        result = {}
        for property in output:
            result = property
            del result['_id']
        return to_json(result)

    def update_property(self, newObj, id):
        output = self.client.find_one_and_update(self.db_name, "properties", {'field_id': id}, {'$set':newObj})
        del output['_id']
        return to_json(output)

    def delete_property(self, service_id, id):
        result = self.client.find_one_and_delete(self.db_name, "properties", {'field_id': id})
        return to_json(result)

    def delete_properties(self, ids):
        results = []
        for id in ids:
            result = self.client.find_one_and_delete(self.db_name, "properties", {'field_id': id})
            results.append(result)
        return results

    def create_property(self, app):
        id = self.client.insert_one(self.db_name, "properties", app).inserted_id
        del  app['_id']
        return to_json(app)