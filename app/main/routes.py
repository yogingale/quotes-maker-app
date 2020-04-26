from app.main import main_bp
from flask import current_app, request, redirect, render_template, url_for
from flask_login import current_user, login_required
from boto3.dynamodb.conditions import Key, Attr

import base64
import random
import boto3

DEFAULT_MOODS = ["love", "death", "life"]


@main_bp.before_app_request
def before_request():
    current_app.logger.debug("in before app request ")


def get_caption_from_response(response):
    return response["Items"][0]["caption"]


def get_caption(
    main_mood: str,
    main_object: str = None,
    sub_mood: str = None,
    sub_object: str = None,
):
    dynamodb = boto3.resource(
        "dynamodb", region_name="us-east-2", endpoint_url="http://localhost:8000"
    )
    table = dynamodb.Table("caption-maker")

    if main_object:
        resp = table.query(
            KeyConditionExpression=Key("main_mood").eq(main_mood)
            & Key("main_object").eq(main_object),
            FilterExpression=(
                Attr("sub_moods").contains(sub_mood)
                | Attr("sub_objects").contains(sub_object)
                | Attr("unknown").not_exists()
            ),
        )
        try:
            return get_caption_from_response(resp)
        except IndexError:
            return get_caption(main_mood, sub_mood=sub_mood, sub_object=sub_object)

    resp = table.query(
        KeyConditionExpression=Key("main_mood").eq(main_mood),
        FilterExpression=(
            Attr("sub_moods").contains(sub_mood)
            | Attr("sub_objects").contains(sub_object)
            | Attr("unknown").not_exists()
        ),
    )
    try:
        return get_caption_from_response(resp)
    except IndexError:
        main_mood = random.choice(DEFAULT_MOODS)
        print(main_mood)
        return get_caption(main_mood)


def get_objects(encoded_image):
    client = boto3.client("rekognition")
    # return client.detect_labels(Image={'Bytes': encoded_image})
    return {
        "LabelModelVersion": "2.0",
        "Labels": [
            {
                "Confidence": 89.40167236328125,
                "Instances": [],
                "Name": "Food",
                "Parents": [],
            },
            {
                "Confidence": 89.40167236328125,
                "Instances": [
                    {
                        "BoundingBox": {
                            "Height": 0.736283004283905,
                            "Left": 0.2987543046474457,
                            "Top": 0.12691982090473175,
                            "Width": 0.3632027208805084,
                        },
                        "Confidence": 89.40167236328125,
                    }
                ],
                "Name": "Ketchup",
                "Parents": [{"Name": "Food"}],
            },
            {
                "Confidence": 67.88510131835938,
                "Instances": [],
                "Name": "Pencil",
                "Parents": [],
            },
        ],
        "ResponseMetadata": {
            "HTTPHeaders": {
                "connection": "keep-alive",
                "content-length": "437",
                "content-type": "application/x-amz-json-1.1",
                "date": "Sun, 26 Apr 2020 01:07:38 GMT",
                "x-amzn-requestid": "40ad4f49-3fd0-4128-9522-ab1613873734",
            },
            "HTTPStatusCode": 200,
            "RequestId": "40ad4f49-3fd0-4128-9522-ab1613873734",
            "RetryAttempts": 0,
        },
    }


@main_bp.route("/upload", methods=["POST"])
def upload():
    print(request.form.to_dict())

    if request.method == "POST":
        moods = request.form.to_dict()
        sorted_moods = sorted(moods.keys(), key=moods.get)
        main_mood = sorted_moods[0]
        sub_mood = sorted_moods[1]

        image = request.files["photo"]
        base64_image = base64.b64encode(image.read())
        base_64_binary = base64.decodebytes(base64_image)
        objects = get_objects(base_64_binary)
        main_object = objects["Labels"][0]["Name"]
        sub_object = objects["Labels"][1]["Name"]
        # print(main_mood)
        caption = get_caption(main_mood, main_object, sub_mood, sub_object)
        return render_template("main/index.html", caption=caption,)


@main_bp.route("/", methods=["GET"])
@main_bp.route("/index", methods=["GET"])
@login_required
def index():
    # return current_app.send_static_file("get-shit-done-1.4.1/index.html")
    return render_template(
        "main/index.html",
        server_message="Flask, Jinja and Creative Tim.. working together!",
    )
