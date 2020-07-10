import os

from app import create_app
from config import Config

app = create_app(config_class=Config)
app.config.from_object(os.environ.get("APP_SETTINGS"))


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    if app.config["APP_STAGE"] == "local":
        app.run(debug=True)
    app.run()
