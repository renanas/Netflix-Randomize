from dotenv import load_dotenv
import os
import traceback
import certifi
from pymongo import MongoClient

load_dotenv()
uri = os.getenv('MONGO_URI')
print('MONGO_URI present:', bool(uri))
print('certifi CA file:', certifi.where())
try:
    client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000)
    print('MongoClient created')
    client.admin.command('ping')
    print('PING OK')
except Exception as e:
    print('Exception during MongoDB connect:')
    traceback.print_exc()
    print('repr:', repr(e))
