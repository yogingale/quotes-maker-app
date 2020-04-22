from app import login_manager
from app.models import User
from flask import current_app
from config import Config
from functools import wraps
from flask_login import current_user
from werkzeug.exceptions import Unauthorized


@login_manager.user_loader
def load_user(id):
    """

    :param id: username
    :return: return User object or None
    """
    # current_app.logger.info(f'load_user: {id}')

    users = Config.load_users()
    for user in users:
        if user["username"] == id:
            return User(user["username"], user["password"], user["roles"], user)

    return None


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
