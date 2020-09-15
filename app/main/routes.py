from app.main import main_bp
from flask import current_app, request, render_template, session, redirect, url_for
from flask_login import current_user, login_required
from app.services.db_services import init_db

from .mongo import MongoManager
from .aws import Rekognition
import base64
import random
import boto3

# User limits
NON_LOGGED_IN_USER_LIMIT = 15
LOGGED_IN_USER_LIMIT = 35

mongo = MongoManager.quotes_maker()


@main_bp.before_app_request
def before_request():
    current_app.logger.debug("in before app request ")


def process_request(request):
    """Process flask request and extract attributes for mongo query."""
    moods = request.form.to_dict()
    sorted_moods = [
        k
        for k, v in sorted(moods.items(), key=lambda item: int(item[1]), reverse=True)
        if int(v) > 0
    ]
    try:
        general_mood = sorted_moods[0]
        moods = sorted_moods[1:6]
    except IndexError:
        general_mood = moods = None

    sorted_objects = None
    if request.files["photo"]:
        image = request.files["photo"]
        base64_image = base64.b64encode(image.read())
        base_64_binary = base64.decodebytes(base64_image)
        objects = Rekognition().detect_labels(base_64_binary)
        sorted_objects = [label["Name"].lower() for label in objects["Labels"]][:4]

    current_app.logger.info(
        "general_mood: %s, moods: %s, objects: %s", general_mood, moods, sorted_objects,
    )
    return general_mood, moods, sorted_objects


@main_bp.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        count = session.setdefault("caption_form_usage_count", 0)
        session["caption_form_usage_count"] = count + 1
        if session["caption_form_usage_count"] >= NON_LOGGED_IN_USER_LIMIT:
            return render_template(
                "main/index.html",
                homepage_message="You have crossed the usage limit. Please signup to get more captions.",
            )
        general_mood, moods, sorted_objects = process_request(request)
        captions = mongo.get_captions(
            general_mood=general_mood, moods=moods, objects=sorted_objects
        )
        return render_template("main/index.html", captions=captions, login=False)


@main_bp.route("/upload-login", methods=["POST"])
def upload_login():
    if request.method == "POST":
        count = session.setdefault("caption_form_usage_count", 0)
        session["caption_form_usage_count"] = count + 1
        if session["caption_form_usage_count"] >= LOGGED_IN_USER_LIMIT:
            return render_template(
                "main/index.html",
                homepage_message="You have crossed the usage limit. Please come back tomorrow.",
            )

        general_mood, moods, sorted_objects = process_request(request)
        captions = mongo.get_captions(
            general_mood=general_mood, moods=moods, objects=sorted_objects
        )
        return render_template("main/index.html", captions=captions, login=True)


@main_bp.route("/", methods=["GET"])
@main_bp.route("/index", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return render_template(
            "main/index.html",
            server_message="Flask, Jinja and Creative Tim.. working together!",
            login=True,
        )
    session.setdefault("caption_form_usage_count", 0)
    if session["caption_form_usage_count"] >= NON_LOGGED_IN_USER_LIMIT:
        return render_template(
            "main/index.html",
            homepage_message="You have crossed the usage limit. Please signup to get more captions.",
            login=False,
        )
    return render_template(
        "main/index.html",
        server_message="Flask, Jinja and Creative Tim.. working together!",
        login=False,
    )
