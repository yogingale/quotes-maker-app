from app import create_app
from config import Config

app = create_app(config_class=Config)

# TODO : host site
# TODO : Add a button to disable moods
# TODO : Make upload form beautiful
# TODO : Fix css of moods
# TODO : Add app.run based on environment.
# TODO : Remove extra packages from requirements
# TODO : Fix domain name
# TODO : purchase domain name

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host="0.0.0.0")

    # app.run()
