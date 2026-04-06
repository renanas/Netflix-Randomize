from backend.database.mongodb_connection import MongoDBConnection
from datetime import datetime


class RecommendationRepository:
    def __init__(self):
        self.mongo_conn = MongoDBConnection(collection_name="recommendations")
        if not self.mongo_conn.connect():
            raise RuntimeError("Failed to connect to MongoDB")
        self.db = self.mongo_conn.get_db()
        if self.db is None:
            raise RuntimeError("Database connection failed: db is None")
        self.collection = self.db["recommendations"]

    def upsert_recommendations(self, user_id: str, movie_ids: list):
        now = datetime.utcnow().isoformat()
        self.collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "movie_ids": movie_ids,
                    "updated_at": now,
                }
            },
            upsert=True,
        )

    def get_recommendations(self, user_id: str):
        doc = self.collection.find_one({"user_id": user_id})
        if not doc:
            return None
        return doc.get("movie_ids", [])

    def delete_recommendations(self, user_id: str):
        self.collection.delete_one({"user_id": user_id})
