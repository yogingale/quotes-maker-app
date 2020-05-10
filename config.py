import os
import urllib

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

users = [
    {
        "username": "user1",
        "password": "user1",
        "roles": ["USER"],
        "email_address": "user1@example.com",
        "first_name": "First",
        "last_name": "User",
        "street_address": "100 Main Street",
        "city": "Mayberry",
        "postal_code": "021344",
        "about_me": "Little of this, little of that",
    },
    {
        "username": "user2",
        "password": "user2",
        "roles": ["USER"],
        "email_address": "user2@example.com",
        "first_name": "Second",
        "last_name": "User",
        "street_address": "200 Main Street",
        "city": "Winslow",
        "postal_code": "123456",
        "about_me": "standing on a street corner",
    },
    {
        "username": "user3",
        "password": "user3",
        "roles": ["USER"],
        "email_address": "user3@example.com",
        "first_name": "Third",
        "last_name": "User",
        "street_address": "1 south NorthWest",
        "city": "Confused",
        "postal_code": "66666",
        "about_me": "Looking everywhere for no where",
    },
    {
        "username": "admin",
        "password": "admin",
        "roles": ["ADMIN"],
        "email_address": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "street_address": "333 North Street",
        "city": "Boston",
        "postal_code": "09876",
        "about_me": "I am the king - its good to be king",
    },
]


class Config(object):
    # needed by flask wtf for CSRC
    SECRET_KEY = os.environ.get("SECRET_KEY") or "YOU WILL NEVER GUESS"
    CSRF_ENABLED = True
    CONTENT_DIR = "get-shit-done-1.4.1"
    STATIC_PATH = f"static/{CONTENT_DIR}"
    TEMPLATES_DIR = f"templates/{CONTENT_DIR}"
    MONGO_DB_PASSWORD = urllib.parse.quote_plus(os.environ.get("MONGO_DB_PASSWORD"))
    MONGO_DB_URI = f"mongodb+srv://caption-maker:{MONGO_DB_PASSWORD}@cluster0-9y16x.mongodb.net/test?retryWrites=true&w=majority"

    @staticmethod
    def load_users():
        """
        function to return a collection of json objects representing the
        :return:
        """
        return users
