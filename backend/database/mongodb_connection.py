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
            raise ValueError("MONGO_URI não definida no .env ou não fornecida")
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Estabelece a conexão com o MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            # Testa a conexão
            self.client.admin.command("ping")
            print("Conectado com sucesso!")
            return True
        except Exception as e:
            print(f"Falha ao conectar: {e}")
            self.client = None
            self.db = None
            self.collection = None
            return False

    def disconnect(self):
        """Fecha a conexão."""
        if self.client:
            self.client.close()
            print("Conexão fechada.")

    def get_collection(self):
        """Retorna a coleção."""
        return self.collection

    def get_db(self):
        """Retorna o banco de dados."""
        return self.db