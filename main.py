import os

from app import create_app
from config import Config

app = create_app(config_class=Config)
app.config.from_object(os.environ.get("APP_SETTINGS"))

# TODO : Add google signup
# TODO : Add adds
# TODO : Add a button to disable moods
# TODO : Add down arrow on banner when submit for action
# TODO : create carousal banner
# TODO : restructure python code
# TODO : Add main/app.run based on environment.
# TODO : purchase domain
# TODO : Add MONGO_DB_URI in env variable
# TODO : Replace prints with logs
# TODO : Check GDPR constraints
# TODO : Add transperant nav bar from creative-tim

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    # app.run(debug=True)

    app.run()
