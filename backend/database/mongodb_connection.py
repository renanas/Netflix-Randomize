from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDBConnection:
    def __init__(self, uri=None, db_name=None, collection_name="movies"):
        self.uri = uri or os.getenv("MONGO_URI")
        self.db_name = db_name or os.getenv("DB_NAME", "netflix")
        self.collection_name = collection_name
        if not self.uri:
            raise ValueError("MONGO_URI not defined in .env or not provided")
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Establishes the connection with MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            # Test the connection
            self.client.admin.command("ping")
            print("Connected successfully!")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.client = None
            self.db = None
            self.collection = None
            return False

    def disconnect(self):
        """Closes the connection."""
        if self.client:
            self.client.close()
            print("Connection closed.")

    def get_collection(self):
        """Returns the collection."""
        return self.collection

    def get_db(self):
        """Returns the database."""
        return self.db