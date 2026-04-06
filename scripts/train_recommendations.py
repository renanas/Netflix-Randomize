#!/usr/bin/env python
"""
Batch script to train KNN recommendation model.

Usage:
    python scripts/train_recommendations.py

This script:
1. Connects to MongoDB
2. Fetches all movies from the database
3. Extracts features (genres, popularity, ratings, etc)
4. Trains a K-Nearest Neighbors model
5. Saves the model for use by the API
"""

import sys
import os

# Add recommendation_system to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recommendation_system.train_model import train_knn_model

if __name__ == "__main__":
    print("Starting KNN model training...")
    try:
        train_knn_model(n_neighbors=10)
        print("✓ Model training completed successfully!")
    except Exception as e:
        print(f"✗ Training failed: {e}")
        sys.exit(1)
