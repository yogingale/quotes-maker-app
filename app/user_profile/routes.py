from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from app.user_profile import user_profile_bp
from app.services import auth_services
from app.user_profile.forms import UserProfileForm


@user_profile_bp.route("/user_profile", methods=["GET", "POST"])
@login_required
def user_profile():
    form = UserProfileForm()
    current_app.logger.info(f"User: {current_user}")
    loggedin_user = auth_services.load_user(id=current_user.id)
    if form.validate_on_submit():
        user = auth_services.load_user(id=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("user_profile.user"))
        return redirect(url_for("user_profile.user"))
    return render_template(
        "user_profile/user.html", title="User Profile", form=form, user=current_user
    )
