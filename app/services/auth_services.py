from app import login_manager
from app.models import User
from flask import current_app
from config import Config
import pymongo
import urllib
from functools import wraps
from flask_login import current_user
from werkzeug.exceptions import Unauthorized


@login_manager.user_loader
def load_user(id):
    """Load user from DB

    :param id: username
    :return: return User object or None
    """
    print(id)
    # current_app.logger.info(f'load_user: {id}')
    client = pymongo.MongoClient("localhost", 27017)
    password = urllib.parse.quote_plus("Dhoni@12345")
    client = pymongo.MongoClient(
        f"mongodb+srv://caption-maker:{password}@cluster0-9y16x.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.caption_maker
    users = db.users

    response = users.find({"email": id})
    for user in response:
        if user["email"] == id:
            return User(
                user["username"], user["password"], user["roles"], user["email"], user
            )

    return None


def create_user(data):
    """Create user in DB/

    :param data: user data
    :return: return User status
    """
    # current_app.logger.info(f'load_user: {id}')
    client = pymongo.MongoClient("localhost", 27017)
    password = urllib.parse.quote_plus("Dhoni@12345")
    client = pymongo.MongoClient(
        f"mongodb+srv://caption-maker:{password}@cluster0-9y16x.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client.caption_maker
    users = db.users
    data = {
        "username": data["username"],
        "password": data["password"],
        "email": data["email"],
        "roles": ["user"],
    }

    users.insert_one(data)

    return True


def get_current_user_roles():
    if current_user:
        return current_user.roles
    else:
        return []


def error_response():
    raise Unauthorized()


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not set(get_current_user_roles()).intersection(set(roles[0])):
                return error_response()
            return f(*args, **kwargs)

        return wrapped

    return wrapper
