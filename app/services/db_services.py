import pymongo
from flask import current_app
import ssl

def init_db():

    if current_app.config.get("APP_STAGE") == "local":
        client = pymongo.MongoClient(current_app.config.get("MONGO_DB_URI"),ssl_cert_reqs=ssl.CERT_NONE)
        return client
    client = pymongo.MongoClient(current_app.config.get("MONGO_DB_URI"))
    return client
