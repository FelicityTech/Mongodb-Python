from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://felicitytechcluster.wbx2syw.mongodb.net/ --apiVersion 1 --username FelicityTech"
client = MongoClient(MONGODB_URI)
for db_name in client.list_database_names():
    print(db_name)