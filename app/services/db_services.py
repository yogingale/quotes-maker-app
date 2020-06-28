import pymongo
from flask import current_app

def init_db():
    client = pymongo.MongoClient(current_app.config.get("MONGO_DB_URI"))
    return client
