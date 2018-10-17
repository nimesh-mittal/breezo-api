from pymongo import MongoClient, ReturnDocument, ASCENDING


class MongoDBClient:
    def __init__(self):
        self.url = 'localhost:27017'
        self.db_client = MongoClient(self.url, appname='breezo_api')

    def insert_one(self, db_name, collection_name, data):
        db = self.db_client[db_name]
        if db is None:
            raise ConnectionError(self.error)
        return db[collection_name].insert_one(data)

    def find(self, db_name, collection_name, query={}, offset=0, limit=1, sort_field="_id", sort_order=ASCENDING):
        db = self.db_client[db_name]

        if db is None:
            raise ConnectionError(self.error)

        results = []
        print("running find on collection {} with limit={} offset={} query={}".format(collection_name, limit, offset, query))

        db_results = db[collection_name].find(query).sort(sort_field, sort_order).skip(int(offset)).limit(int(limit))

        results_count = db_results.count()
        for result in db_results:
            results.append(result)

        self.db_client.close()

        return results, results_count

    def find_one_and_update(self, db_name, collection_name, query, update):
        db = self.db_client[db_name]

        if db is None:
            raise ConnectionError(self.error)

        return db[collection_name].find_one_and_update(query, update, return_document=ReturnDocument.AFTER)

    def find_one_and_delete(self, db_name, collection_name, query):
        db = self.db_client[db_name]

        if db is None:
            raise ConnectionError(self.error)

        return db[collection_name].find_one_and_delete(query, projection={'_id': False})

    def close(self):
        return self.db_client.close()

db_client = MongoDBClient()