from flask import Flask, render_template

from flask import (
    current_app,
    request,
    render_template,
    session,
    redirect,
    url_for,
    abort,
    make_response,
    jsonify,
)
from flask_login import current_user, login_required

from services.mongo import MongoManager, DEFAULT_TOPICS
from services.aws import Rekognition
import base64
import random
import boto3
from datetime import datetime

import os

from config import Config, create_app

app = create_app(config_class=Config)

# User limits
# NON_LOGGED_IN_USER_LIMIT = 15
# LOGGED_IN_USER_LIMIT = 35


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html"), 404


# def process_image_request(request):
#     """Process flask request and extract attributes for mongo query."""
#     moods = request.form.to_dict()
#     sorted_moods = [
#         k
#         for k, v in sorted(moods.items(), key=lambda item: int(item[1]), reverse=True)
#         if int(v) > 0
#     ]
#     try:
#         general_mood = sorted_moods[0]
#         moods = sorted_moods[1:6]
#     except IndexError:
#         general_mood = moods = None

#     sorted_objects = None
#     if request.files["photo"]:
#         image = request.files["photo"]
#         base64_image = base64.b64encode(image.read())
#         base_64_binary = base64.decodebytes(base64_image)
#         objects = Rekognition().detect_labels(base_64_binary)
#         sorted_objects = [label["Name"].lower() for label in objects["Labels"]][:4]

#     current_app.logger.info(
#         "general_mood: %s, moods: %s, objects: %s", general_mood, moods, sorted_objects,
#     )
#     return general_mood, moods, sorted_objects


# @main_bp.route("/upload", methods=["POST"])
# def upload():
#     if request.method == "POST":
#         count = session.setdefault("caption_form_usage_count", 0)
#         session["caption_form_usage_count"] = count + 1
#         if session["caption_form_usage_count"] >= NON_LOGGED_IN_USER_LIMIT:
#             return render_template(
#                 "main/index.html",
#                 homepage_message="You have crossed the usage limit. Please signup to get more captions.",
#             )
#         general_mood, moods, sorted_objects = process_image_request(request)
#         resp = mongo.get_quotes(
#             general_mood=general_mood, moods=moods, objects=sorted_objects
#         )
#         return render_template(
#             "main/index.html", captions=resp["captions"], login=False
#         )


# @main_bp.route("/upload-login", methods=["POST"])
# def upload_login():
#     if request.method == "POST":
#         count = session.setdefault("caption_form_usage_count", 0)
#         session["caption_form_usage_count"] = count + 1
#         if session["caption_form_usage_count"] >= LOGGED_IN_USER_LIMIT:
#             return render_template(
#                 "main/index.html",
#                 homepage_message="You have crossed the usage limit. Please come back tomorrow.",
#             )

#         general_mood, moods, sorted_objects = process_image_request(request)
#         resp = mongo.get_quotes(
#             general_mood=general_mood, moods=moods, objects=sorted_objects
#         )
#         return render_template(
#             "main/index.html",
#             captions=resp["captions"],
#             keywords=resp["keywords"],
#             login=True,
#         )


# @main_bp.route("/", methods=["GET"])
# @main_bp.route("/index", methods=["GET"])
# def index():
#     if current_user.is_authenticated:
#         return render_template(
#             "main/index.html",
#             server_message="Flask, Jinja and Creative Tim.. working together!",
#             login=True,
#         )
#     session.setdefault("caption_form_usage_count", 0)
#     if session["caption_form_usage_count"] >= NON_LOGGED_IN_USER_LIMIT:
#         return render_template(
#             "main/index.html",
#             homepage_message="You have crossed the usage limit. Please signup to get more captions.",
#             login=False,
#         )
#     return render_template(
#         "main/index.html",
#         server_message="Flask, Jinja and Creative Tim.. working together!",
#         login=False,
#     )


# @main_bp.route("/mood/<mood>", methods=["GET"])
# def captions_on_moods(mood):
#     if mood not in DEFAULT_MOODS:
#         return (
#             render_template("errors/404.html", error_message=f"Mood {mood} not Found!"),
#             404,
#         )
#     if request.method == "GET":
#         resp = mongo.get_quotes(general_mood=mood)
#         return render_template(
#             "main/index.html",
#             captions=resp["captions"],
#             keywords=resp["keywords"],
#             login=False,
#         )


# @main_bp.route("/author/<author>", methods=["GET"])
# def captions_on_author(author):
#     if request.method == "GET":
#         resp = mongo.get_quotes_based_on_author(author)
#         return render_template(
#             "main/index.html",
#             captions=resp["captions"],
#             keywords=resp["keywords"],
#             login=False,
#         )


# @main_bp.route("/sitemap.xml")
# def site_map():
#     moods = DEFAULT_MOODS
#     page_ids = range(1, 11)
#     lastmod = datetime.today().strftime("%Y-%m-%d")

#     pages = [{"mood": "love", "pageID": 1, "modified": "2020-12-27"}]

#     pages = []
#     for mood in moods:
#         for page_id in page_ids:
#             pages.append({"mood": mood, "pageID": page_id, "modified": lastmod})

#     print(pages)

#     sitemap_xml = render_template(
#         "sitemap_template.xml",
#         pages=pages,
#         base_url="https://quotes-maker.com",
#     )
#     response = make_response(sitemap_xml)
#     response.headers["Content-Type"] = "application/xml"

#     return response


# @main_bp.route("/", methods=["GET"])
# @main_bp.route("/index", methods=["GET"])
# def index():
#     if current_user.is_authenticated:
#         return render_template(
#             "main/index.html",
#             server_message="Flask, Jinja and Creative Tim.. working together!",
#             login=True,
#         )
#     session.setdefault("caption_form_usage_count", 0)
#     if session["caption_form_usage_count"] >= NON_LOGGED_IN_USER_LIMIT:
#         return render_template(
#             "main/index.html",
#             homepage_message="You have crossed the usage limit. Please signup to get more captions.",
#             login=False,
#         )
#     return render_template(
#         "main/index.html",
#         server_message="Flask, Jinja and Creative Tim.. working together!",
#         login=False,
#     )


@app.route("/topic/<topic>")
def topic(topic):
    mongo = MongoManager.quotes_maker()

    if topic not in DEFAULT_TOPICS:
        return abort(404)
    if request.method == "GET":
        resp = mongo.get_quotes(general_mood=topic, order_by_likes=True)
        return render_template("index.html", quotes=resp["quotes"])


@app.route("/like", methods=["POST"])
def like():
    like_data = request.form.to_dict()["data"]
    print(like_data)
    id, count = like_data.split("_")

    count = MongoManager.quotes_maker().like_quote(id)
    return jsonify({"result": "success", "like_count": count})


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html",)


@app.route("/test", methods=["GET"])
def test():
    mongo = MongoManager.quotes_maker()
    mongo.get_quotes(general_mood="funny", order_by_likes=True)
    return jsonify({"result": "success", "like_count": "count"})

if __name__ == "__main__":
    app.run(debug=True)
