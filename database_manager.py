from pymongo import MongoClient


class DatabaseManager:
    def __init__(self, database_name, host, port):
        self.database_name = database_name
        self.host = host
        self.port = port
        self.client = None
        self.collection = None

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

    def create_collection(self, model: str):
        # self.db.create_tables(models)
        collection = self.mongo_db.list_collection_names()

        if model in collection:
            self.collection = self.mongo_db.get_collection(model)
        else:
            self.collection = self.mongo_db[model]
