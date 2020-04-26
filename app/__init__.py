import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager

from app.context_processors import is_active_link
from app.flask_csrf_test_client import FlaskCSRFClient

login_manager = LoginManager()


def create_app(config_class=None):
    app = Flask(
        __name__,
        static_url_path="",
        static_folder=config_class.STATIC_PATH,
        template_folder=config_class.TEMPLATES_DIR,
    )
    app.config.from_object(config_class)

    # override the default test_client with one that support csrf
    # forms
    app.test_client_class = FlaskCSRFClient

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

    from app.tables import tables_bp as tables_bp

    app.register_blueprint(tables_bp, url_prefix="/tables")

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
    except:
        # if there is some reason we cannot create the file handler then just pass
        # I have seen this happen when deploying to AWS via zappa
        pass

    # add functions to jinja template engine
    app.jinja_env.globals.update(is_active_link=is_active_link)

    return app
