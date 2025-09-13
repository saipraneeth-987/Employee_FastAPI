# database.py
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

# MongoDB connection (local)
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)

DB_NAME = "assessment_db"
COLLECTION_NAME = "employees"

db = client[DB_NAME]
employees_collection = db[COLLECTION_NAME]

#creating_index
employees_collection.create_index([("employee_id", ASCENDING)], unique=True)

