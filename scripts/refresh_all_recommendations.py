#!/usr/bin/env python
"""
Batch script to refresh recommendations for all users.

Usage:
    python scripts/refresh_all_recommendations.py

This script:
1. Connects to MongoDB
2. Fetches all user IDs
3. For each user, computes recommendations using KNN
4. Saves results to the recommendations collection
"""

import sys
import os
import logging

# Add paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient
from backend.services.recommendation_service import RecommendationService
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def refresh_all_recommendations():
    """Refresh recommendations for all users."""
    
    # Connect to MongoDB
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "netflix")
    
    if not uri:
        raise ValueError("MONGO_URI not set in .env")
    
    client = MongoClient(uri)
    db = client[db_name]
    users_collection = db["users"]
    
    # Fetch all user IDs
    logger.info("Fetching all users...")
    users = list(users_collection.find({}, {"_id": 1}))
    logger.info(f"Found {len(users)} users")
    
    # Initialize service
    service = RecommendationService()
    
    # Process each user
    success_count = 0
    error_count = 0
    
    for user in users:
        user_id = str(user["_id"])
        try:
            logger.info(f"Processing user {user_id}...")
            service.build_recommendations_for_user(user_id, limit=20)
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to process user {user_id}: {e}")
            error_count += 1
    
    logger.info(f"\nBatch complete!")
    logger.info(f"✓ Success: {success_count}")
    logger.info(f"✗ Errors: {error_count}")


if __name__ == "__main__":
    try:
        refresh_all_recommendations()
    except Exception as e:
        logger.error(f"Batch job failed: {e}")
        sys.exit(1)
