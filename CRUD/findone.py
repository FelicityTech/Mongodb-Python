import os
import pprint

from dotenv import load_dotenv
from pymongo import MongoClient

# import ObjectId from bson package (part of PyMongo distribution) to enable querying by ObjectId
from bson.objectid import ObjectId

# Load config from .env file
load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

# Connect to MongoDB cluster with MongoClient
client = MongoClient(MONGODB_URI)

# Get reference to 'bank' database
# db = client.bank
db = client["bank"]
# Get reference to 'accounts' collection
accounts_collection = db.accounts

# Query by ObjectId
document_to_find = {"_id": ObjectId("65143e38f07d13fe75a0c971")}

# Write an expression that retrieves the documentg matching the query constraint in the "account" collection.
result = accounts_collection.find_one(document_to_find)
pprint.pprint(result)

client.close()