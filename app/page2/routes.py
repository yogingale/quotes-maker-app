from app.page2 import page2_bp
from flask import current_app, request, redirect, render_template
from flask_login import current_user, login_required


@page2_bp.before_app_request
def before_request():
    current_app.logger.debug("in before page2 app request ")


@page2_bp.route("/index", methods=["GET"])
@login_required
def index():
    # return current_app.send_static_file("get-shit-done-1.4.1/index.html")
    return render_template(
        "page2/index.html",
        server_message="Flask, Jinja and Creative Tim.. working together!",
    )
