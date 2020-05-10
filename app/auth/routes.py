from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app.auth import auth_bp
from app.auth.forms import LoginForm, SignupForm
from app.services import auth_services


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = auth_services.load_user(id=form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username/email or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template(
        "auth/login.html",
        title="Sign In",
        form=form,
        server_message="Example Login page using Creative Tim Template and Flask",
    )


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SignupForm()
    if form.validate_on_submit():
        user = auth_services.load_user(id=form.email.data)
        if user:
            flash("Email address already exists. Try with different email.")
            return redirect(url_for("auth.signup"))
        auth_services.create_user(data=form.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template(
        "auth/signup.html",
        title="Sign In",
        form=form,
        server_message="Example signup page using Creative Tim Template and Flask",
    )


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
