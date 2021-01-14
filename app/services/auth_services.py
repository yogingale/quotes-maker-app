from app import login_manager
from app.models import User
from flask_login import current_user
from flask import current_app
from werkzeug.exceptions import Unauthorized
from app.services.mongo import MongoManager

mongo = MongoManager.quotes_maker()


@login_manager.user_loader
def load_user(id):
    """Load user from DB

    :param id: username
    :return: return User object or None
    """

    current_app.logger.info(f"load_user: {id}")
    users = mongo.get_users(id)
    for user in users:
        if user.email == id:
            return User(user.username, user.password, user.roles, user.email)

    return None


def create_user(data):
    """Create user in DB/

    :param data: user data
    :return: return User status
    """
    current_app.logger.info(f"load_user: {id}")
    mongo.create_user(
        username=data["username"],
        password=data["password"],
        email=data["email"],
        roles="user",
    )

    return True


def get_current_user_roles():
    if current_user:
        return current_user.roles
    else:
        return []


def error_response():
    raise Unauthorized()
