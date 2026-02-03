from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

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
            logger.info("Connected to MongoDB successfully")
            return True
        except Exception as e:
            logger.exception("Failed to connect to MongoDB")
            self.client = None
            self.db = None
            self.collection = None
            return False

    def disconnect(self):
        """Closes the connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    def get_collection(self):
        """Returns the collection."""
        return self.collection

    def get_db(self):
        """Returns the database."""
        return self.db