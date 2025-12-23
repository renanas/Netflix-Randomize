import os
from dotenv import load_dotenv

load_dotenv()

print("MONGO_URI =", repr(os.getenv("MONGO_URI")))
print("DB_NAME =", repr(os.getenv("DB_NAME")))
