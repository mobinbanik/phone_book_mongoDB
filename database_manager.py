from pymongo import MongoClient


class DatabaseManager:
    def __init__(self, database_name, host, port):
        self.database_name = database_name
        self.host = host
        self.port = port
        self.client = None

        self.mongo_db = self.connect_to_database()

    def connect_to_database(self):
        self.client = MongoClient(
            host=self.host,
            port=self.port,
        )
        mongo_db = self.client[self.database_name]
        return mongo_db

    def close_connection(self):
        self.client.close()

    def create_collection(self, model="contacts"):
        # self.db.create_tables(models)
        collection = self.mongo_db.list_collection_names()

        if model in collection:
            return self.mongo_db.get_collection(model)
        else:
            return self.mongo_db[model]
