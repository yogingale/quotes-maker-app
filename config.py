"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv
import urllib
import os
from flask import Flask

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY") or "YOU WILL NEVER GUESS"
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    FLASK_ENV = os.environ["APP_STAGE"]


class ProdConfig(Config):
    DEBUG = False
    TESTING = False

    # MongoDB
    MONGO_DB_PASSWORD = urllib.parse.quote_plus(os.environ.get("MONGO_DB_PASSWORD"))
    MONGO_DB_NAME = urllib.parse.quote_plus(os.environ.get("MONGO_DB_NAME"))
    MONGO_DB_URI = f"mongodb+srv://caption-maker:{MONGO_DB_PASSWORD}@cluster0-9y16x.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority"


class DevConfig(Config):
    DEBUG = True
    TESTING = True

    # MongoDB
    MONGO_DB_PASSWORD = urllib.parse.quote_plus(os.environ.get("MONGO_DB_PASSWORD"))
    MONGO_DB_NAME = urllib.parse.quote_plus(os.environ.get("MONGO_DB_NAME"))
    MONGO_DB_URI = f"mongodb+srv://caption-maker:{MONGO_DB_PASSWORD}@cluster0-9y16x.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority"


def create_app(config_class=None):
    app = Flask(
        __name__,
        static_url_path="",
        static_folder=config_class.STATIC_FOLDER,
        template_folder=config_class.TEMPLATES_FOLDER,
    )
    app_stage = config_class.FLASK_ENV

    # TODO: Implement this using switch-case from python 3.10
    if app_stage == "local" or app_stage == "dev":
        # Using a development configuration
        app.config.from_object("config.DevConfig")

    if app_stage == "prod":
        # Using a production configuration
        app.config.from_object("config.ProdConfig")

    return app
