"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv
import urllib
import os

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY") or "YOU WILL NEVER GUESS"
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class ProdConfig(Config):
    FLASK_ENV = os.environ["APP_STAGE"]
    DEBUG = False
    TESTING = False

    # MongoDB
    MONGO_DB_PASSWORD = urllib.parse.quote_plus(os.environ.get("MONGO_DB_PASSWORD"))
    MONGO_DB_NAME = urllib.parse.quote_plus(os.environ.get("MONGO_DB_NAME"))
    MONGO_DB_URI = f"mongodb+srv://caption-maker:{MONGO_DB_PASSWORD}@cluster0-9y16x.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority"


class DevConfig(Config):
    FLASK_ENV = os.environ["APP_STAGE"]
    DEBUG = True
    TESTING = True

    # MongoDB
    MONGO_DB_PASSWORD = urllib.parse.quote_plus(os.environ.get("MONGO_DB_PASSWORD"))
    MONGO_DB_NAME = urllib.parse.quote_plus(os.environ.get("MONGO_DB_NAME"))
    MONGO_DB_URI = f"mongodb+srv://caption-maker:{MONGO_DB_PASSWORD}@cluster0-9y16x.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority"
