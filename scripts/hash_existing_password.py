import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.database.mongodb_connection import MongoDBConnection
from backend.utils.auth import get_password_hash

# Conectar ao banco
mongo_conn = MongoDBConnection()
mongo_conn.connect()
db = mongo_conn.get_db()
collection = db["users"]

# Encontrar o usuário
user = collection.find_one({"email": "user@example.com"})
if user:
    # Hashear a senha atual (que está em texto plano)
    hashed_password = get_password_hash(user['senha'])
    # Atualizar no banco
    collection.update_one({"_id": user["_id"]}, {"$set": {"senha": hashed_password}})
    print("Senha hasheada e atualizada com sucesso!")
else:
    print("Usuário não encontrado.")

mongo_conn.close()