from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "netflix_clone")

if not MONGO_URI:
    raise ValueError("MONGO_URI não definida no .env")

client = MongoClient(MONGO_URI)

try:
    client.admin.command("ping")
    print("✅ Conectado ao MongoDB")
except Exception as e:
    print("❌ Falha ao conectar no MongoDB:", e)
    raise

db = client[DB_NAME]
