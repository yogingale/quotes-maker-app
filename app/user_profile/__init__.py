from flask import Blueprint

user_profile_bp = Blueprint("user", __name__)

from app.user_profile import routes, forms
