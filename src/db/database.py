import os
from pymongo import MongoClient
from pymongo.database import Database

class DatabaseManager:
    client: MongoClient = None
    db_name: str = os.getenv("DATABASE_NAME", "vehicles_db")

    @classmethod
    def connect(cls):
        mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        cls.client = MongoClient(mongo_url)
        print(f"Connected to MongoDB at {mongo_url}")

    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()
            print("Closed MongoDB connection")

    @classmethod
    def get_db(cls) -> Database:
        if cls.client is None:
            # Lazy connect or raise error. For simplicity, we assume connect called at startup.
            cls.connect()
        return cls.client[cls.db_name]

def get_database() -> Database:
    return DatabaseManager.get_db()
