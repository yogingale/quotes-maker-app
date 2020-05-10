from app.admin import admin_bp
from flask import render_template
from flask_login import login_required


@admin_bp.route("/", methods=["GET"])
@admin_bp.route("/index", methods=["GET"])
@login_required
def index():
    # return current_app.send_static_file("get-shit-done-1.4.1/index.html")
    return render_template(
        "admin/index.html", server_message="Protected for ADMIN ONLY"
    )
