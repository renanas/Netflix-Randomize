import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.database.mongo_connection import db

def main():
    try:
        collections = db.list_collection_names()
        print("✅ Conexão OK. Collections:", collections)
    except Exception as e:
        print("❌ Erro ao usar o MongoDB:", e)

if __name__ == "__main__":
    main()
