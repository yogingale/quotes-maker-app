import os
import urllib

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    # needed by flask wtf for CSRC
    SECRET_KEY = os.environ.get("SECRET_KEY") or "YOU WILL NEVER GUESS"
    CSRF_ENABLED = True
    CONTENT_DIR = "caption-maker"
    STATIC_PATH = f"static/{CONTENT_DIR}"
    TEMPLATES_DIR = f"templates/{CONTENT_DIR}"
    MONGO_DB_PASSWORD = urllib.parse.quote_plus(os.environ.get("MONGO_DB_PASSWORD"))
    MONGO_DB_NAME = urllib.parse.quote_plus(os.environ.get("MONGO_DB_NAME"))
    MONGO_DB_URI = f"mongodb+srv://caption-maker:{MONGO_DB_PASSWORD}@cluster0-9y16x.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority"
