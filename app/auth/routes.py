import functools
import os
import uuid

import flask
import google.oauth2.credentials
import googleapiclient.discovery
from authlib.client import OAuth2Session
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.auth import auth_bp
from app.auth.forms import LoginForm, SignupForm
from app.services import auth_services

ACCESS_TOKEN_URI = "https://www.googleapis.com/oauth2/v4/token"
AUTHORIZATION_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent"
)

AUTHORIZATION_SCOPE = "openid email profile"

AUTH_REDIRECT_URI = os.environ.get("FN_AUTH_REDIRECT_URI", default=False)
BASE_URI = os.environ.get("FN_BASE_URI", default=False)
CLIENT_ID = os.environ.get("FN_CLIENT_ID", default=False)
CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET", default=False)

AUTH_TOKEN_KEY = "auth_token"
AUTH_STATE_KEY = "auth_state"


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
        # server_message="Example Login page using Creative Tim Template and Flask",
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
        # server_message="Example signup page using Creative Tim Template and Flask",
    )


@auth_bp.route("/logout")
def logout():
    logout_user()
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)
    return redirect(url_for("main.index"))


def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False


def build_credentials():
    if not is_logged_in():
        raise Exception("User must be logged in")

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]

    return google.oauth2.credentials.Credentials(
        oauth2_tokens["access_token"],
        refresh_token=oauth2_tokens["refresh_token"],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI,
    )


def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
        "oauth2", "v2", credentials=credentials
    )

    return oauth2_client.userinfo().get().execute()


def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return functools.update_wrapper(no_cache_impl, view)


@auth_bp.route("/google/login")
def google_login():
    session = OAuth2Session(
        CLIENT_ID,
        CLIENT_SECRET,
        scope=AUTHORIZATION_SCOPE,
        redirect_uri=AUTH_REDIRECT_URI,
    )

    uri, state = session.authorization_url(AUTHORIZATION_URL)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True

    return flask.redirect(uri, code=302)


@auth_bp.route("/google/auth")
@no_cache
def google_auth_redirect():
    req_state = flask.request.args.get("state", default=None, type=None)

    if req_state != flask.session[AUTH_STATE_KEY]:
        response = flask.make_response("Invalid state parameter", 401)
        return response

    session = OAuth2Session(
        CLIENT_ID,
        CLIENT_SECRET,
        scope=AUTHORIZATION_SCOPE,
        state=flask.session[AUTH_STATE_KEY],
        redirect_uri=AUTH_REDIRECT_URI,
    )

    oauth2_tokens = session.fetch_access_token(
        ACCESS_TOKEN_URI, authorization_response=flask.request.url
    )

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens
    user_info = get_user_info()
    user = auth_services.load_user(id=user_info["email"])
    if not user:
        auth_services.create_user(
            data={
                "username": user_info["name"],
                "password": str(uuid.uuid4()),
                "email": user_info["email"],
            }
        )
        user = auth_services.load_user(id=user_info["email"])
    login_user(user, remember=True)

    return redirect(url_for("main.index"))
