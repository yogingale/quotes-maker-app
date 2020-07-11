from flask import Blueprint

page2_bp = Blueprint("page2", __name__)

from app.page2 import routes
