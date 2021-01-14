import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from flask_login import LoginManager


login_manager = LoginManager()


def is_active_link(link_names):
    """
    check the passed in collection of link names with the current
    url.  If there is a match, return 'active', else empty string

    Typical usage:
    <li class="{{ is_active_link( [url_for('user.user_profile')] ) }}">


    :param link_names: collection of link names.
    :return: string 'active' is the current url matches the parameter, else empty string.
    """
    current_url_rule = request.url_rule.rule
    if current_url_rule in link_names:
        return "active"
    else:
        return ""


def create_app(config_class=None):
    app = Flask(
        __name__,
        static_url_path="",
        static_folder=config_class.STATIC_PATH,
        template_folder=config_class.TEMPLATES_DIR,
    )
    app.config.from_object(config_class)

    login_manager.init_app(app)

    from app.errors import errors_bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.auth import auth_bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import main_bp as main_bp

    app.register_blueprint(main_bp)

    from app.page2 import page2_bp as page2_bp

    app.register_blueprint(page2_bp, url_prefix="/page2")

    from app.admin import admin_bp as admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.user_profile import user_profile_bp as user_profile_bp

    app.register_blueprint(user_profile_bp, url_prefix="/user")

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    try:
        if not app.debug and not app.testing:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/app_logs.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info("Flask Starter startup")
    except Exception:
        # if there is some reason we cannot create the file handler then just pass
        # I have seen this happen when deploying to AWS via zappa
        pass

    # add functions to jinja template engine
    app.jinja_env.globals.update(is_active_link=is_active_link)

    return app
