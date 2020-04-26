from app import create_app
from config import Config

app = create_app(config_class=Config)

# TODO : Add app.run based on environment.
# TODO : Remove extra packages from requirements
# TODO : Add correct default moods

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host="0.0.0.0")

    # app.run()
