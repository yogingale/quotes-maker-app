from app.main import main_bp
from flask import current_app, request, render_template, session, redirect, url_for
from flask_login import current_user, login_required
from app.services.db_services import init_db

import base64
import random
import boto3

DEFAULT_MOODS = [
    "love",
    "funny",
    "happy",
    "inspiration",
    "weird",
    "random",
    "sad",
    "life",
    "art",
]

DEFAULT_OBJECTS = ["mountain", "sea", "beach", "girl", "boy", "car", "coffee"]

# Caption limits
NUMBER_OF_CAPTIONS = 5

# User limits
NON_LOGGED_IN_USER_LIMIT = 15
LOGGED_IN_USER_LIMIT = 35


@main_bp.before_app_request
def before_request():
    current_app.logger.debug("in before app request ")


def get_captions_from_response(response):
    current_app.logger.info("Response for the captions: %s ", response)
    response = list(response)
    if len(response) >= NUMBER_OF_CAPTIONS:
        number_of_samples = NUMBER_OF_CAPTIONS
    else:
        number_of_samples = len(response)
    random_samples = random.sample(response, number_of_samples)
    captions = []
    current_app.logger.info("Final captions:")
    for sample in random_samples:
        current_app.logger.info(sample)
        captions.append({sample["author"]: sample["caption"]})

    if not captions:
        raise ValueError()

    return captions


def get_caption(
    general_mood: str = None, moods: list = None, objects: list = None,
):
    client = init_db()
    db = client.caption_maker
    captions = db.captions

    if not general_mood:
        if not moods:
            moods = [random.choice(DEFAULT_MOODS)]
        if not objects:
            objects = [random.choice(DEFAULT_OBJECTS)]
        resp = captions.find({"moods": {"$in": moods}, "objects_": {"$in": objects}})
        try:
            return get_captions_from_response(resp)
        except ValueError:
            general_mood = random.choice(DEFAULT_MOODS)
            return get_caption(general_mood, objects, moods)

    if moods and objects:
        resp = captions.find(
            {
                "general_mood": general_mood,
                "moods": {"$in": moods},
                "objects_": {"$in": objects},
            }
        )
        try:
            return get_captions_from_response(resp)
        except ValueError:
            return get_caption(general_mood, objects)

    if moods and not objects:
        resp = captions.find({"general_mood": general_mood, "moods": {"$in": moods},})
        try:
            return get_captions_from_response(resp)
        except ValueError:
            return get_caption(general_mood)

    if not moods and objects:
        resp = captions.find(
            {"general_mood": general_mood, "objects_": {"$in": objects},}
        )
        try:
            return get_captions_from_response(resp)
        except ValueError:
            return get_caption(general_mood)

    if not moods and not objects:
        resp = captions.find({"general_mood": general_mood})
        try:
            return get_captions_from_response(resp)
        except ValueError:
            general_mood = random.choice(DEFAULT_MOODS)
            return get_caption(general_mood)


def get_captions(request):
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
        objects = get_objects(base_64_binary)
        sorted_objects = [label["Name"].lower() for label in objects["Labels"]][:4]

    current_app.logger.info(
        "general_mood: %s, moods: %s, objects: %s", general_mood, moods, sorted_objects,
    )
    captions = get_caption(
        general_mood=general_mood, moods=moods, objects=sorted_objects
    )
    return captions


def get_objects(encoded_image):
    client = boto3.client("rekognition", region_name="us-east-2")
    return client.detect_labels(Image={"Bytes": encoded_image})


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

        captions = get_captions(request)
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

        captions = get_captions(request)
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
