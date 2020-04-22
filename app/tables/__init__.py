from flask import Blueprint

tables_bp = Blueprint("tables", __name__)

from app.tables import routes
