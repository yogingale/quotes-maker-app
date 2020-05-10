from app import login_manager
from app.models import User
from flask_login import current_user
from werkzeug.exceptions import Unauthorized
from app.services.db_services import init_db


@login_manager.user_loader
def load_user(id):
    """Load user from DB

    :param id: username
    :return: return User object or None
    """

    # current_app.logger.info(f'load_user: {id}')
    client = init_db()
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
    client = init_db()
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
