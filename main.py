import os

from app import create_app
from config import Config

app = create_app(config_class=Config)
app.config.from_object(os.environ.get("APP_SETTINGS"))

# TODO : Add a button to disable moods
# TODO : Add login/signup button
# TODO : Add google signup
# TODO : Add adds
# TODO : Add down arrow on banner when submit for action
# TODO : validate form uploads
# TODO : Add homepage button/link
# TODO : create carousal banner
# TODO : restructure python code
# TODO : Remove unnecessary code
# TODO : Add app.run based on environment.
# TODO : purchase domain
# TODO : host site

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host="0.0.0.0")

    # app.run()
