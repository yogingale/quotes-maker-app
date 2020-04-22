from app.admin import admin_bp
from flask import current_app, request, redirect, render_template
from flask_login import current_user, login_required
from ..services.auth_services import requires_roles


@admin_bp.route("/", methods=["GET"])
@admin_bp.route("/index", methods=["GET"])
@login_required
@requires_roles(["ADMIN"])
def index():
    # return current_app.send_static_file("get-shit-done-1.4.1/index.html")
    return render_template(
        "admin/index.html", server_message="Protected for ADMIN ONLY"
    )
