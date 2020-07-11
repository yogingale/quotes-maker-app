import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

users = [
    {"username": "user1", "password": "user1", "roles": ["USER"]},
    {"username": "user2", "password": "user2", "roles": ["USER"]},
    {"username": "user3", "password": "user3", "roles": ["USER"]},
    {"username": "admin", "password": "admin", "roles": ["ADMIN"]},
]


class Config(object):
    # needed by flask wtf for CSRC
    SECRET_KEY = os.environ.get("SECRET_KEY") or "YOU WILL NEVER GUESS"
    # STATIC_PATH = 'static/get-shit-done-1.4.1'
    # TEMPLATES_DIR='templates/get-shit-done-1.4.1'
    # CONTENT_DIR = 'get-shit-done-1.4.1'
    CONTENT_DIR = "pk2-free-v2"
    # CONTENT_DIR = 'paper-dashboard-2'
    STATIC_PATH = f"static/{CONTENT_DIR}"
    TEMPLATES_DIR = f"templates/{CONTENT_DIR}"

    @staticmethod
    def load_users():
        """
        function to return a collection of json objects representing the
        :return:
        """
        return users
