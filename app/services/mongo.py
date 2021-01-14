import os
import urllib
from dataclasses import dataclass, field

from mongoengine import Document, connect
from mongoengine.fields import (
    ListField,
    StringField,
)
import random
from flask import current_app
from pymongo import MongoClient

DEFAULT_MOODS: list = [
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

DEFAULT_OBJECTS: list = ["mountain", "sea", "beach", "girl", "boy", "car", "coffee"]

# Caption limits
NUMBER_OF_CAPTIONS = 5


class Captions(Document):
    caption = StringField(required=True, max_length=250)
    author = StringField(required=True, max_length=50)
    main_mood = StringField(required=True, max_length=50)
    general_mood = StringField(max_length=50)
    moods = ListField(StringField(max_length=50))
    objects_ = ListField(StringField(max_length=50))
    tags = ListField(StringField(max_length=30))


class Users(Document):
    username = StringField(required=True, max_length=250)
    password = StringField(required=True, max_length=50)
    email = StringField(required=True, max_length=50)
    roles = StringField(max_length=50)
    moods = ListField(StringField(max_length=50))
    objects_ = ListField(StringField(max_length=50))
    tags = ListField(StringField(max_length=30))


@dataclass
class MongoManager:
    name: str

    @classmethod
    def quotes_maker(cls):
        return cls("caption_maker")

    def init_db(func):
        """Initialize DB."""

        def wrapper(*args, **kwargs):
            connect("caption_maker", host=current_app.config["MONGO_DB_URI"])
            return func(*args, **kwargs)

        return wrapper

    def get_captions_from_response(self, response: Document) -> dict:
        """Get random samples from mongoengine response, returns captions and keywords."""
        if len(response) >= NUMBER_OF_CAPTIONS:
            number_of_samples = NUMBER_OF_CAPTIONS
        else:
            number_of_samples = len(response)
        random_samples = random.sample(set(response), number_of_samples)
        captions = []
        current_app.logger.info("Final captions:")
        for sample in random_samples:
            current_app.logger.info(sample.caption)
            captions.append({sample.author: sample.caption})
        if not captions:
            raise ValueError()

        keywords = self.get_keywords_from_response(random_samples)
        return {"captions": captions, "keywords": keywords}

    def get_keywords_from_response(self, samples: list) -> str:
        """Generates keywords from samples."""
        keywords = []
        for sample in samples:
            keywords.append(sample.author)
            keywords.extend(sample.moods)
        return ",".join(keywords)

    @init_db
    def get_captions(
        self, general_mood: str = None, moods: list = None, objects: list = None
    ) -> list:
        """Get captions from mongo based on given parameters."""
        if not general_mood:
            if not moods:
                moods = [random.choice(DEFAULT_MOODS)]
            if not objects:
                objects = [random.choice(DEFAULT_OBJECTS)]
            resp = Captions.objects(moods__in=moods, objects___in=objects)
            try:
                return self.get_captions_from_response(resp)
            except ValueError:
                general_mood = random.choice(DEFAULT_MOODS)
                return self.get_caption(general_mood, objects, moods)

        if moods and objects:
            resp = Captions.objects(
                general_mood=general_mood, moods__in=moods, objects___in=objects
            )
            try:
                return self.get_captions_from_response(resp)
            except ValueError:
                return self.get_caption(general_mood, objects)

        if moods and not objects:
            resp = Captions.objects(general_mood=general_mood, moods__in=moods)
            try:
                return self.get_captions_from_response(resp)
            except ValueError:
                return self.get_caption(general_mood)

        if not moods and objects:
            resp = Captions.objects(general_mood=general_mood, objects___in=objects)
            try:
                return self.get_captions_from_response(resp)
            except ValueError:
                return self.get_caption(general_mood)

        if not moods and not objects:
            resp = Captions.objects(general_mood=general_mood)
            try:
                return self.get_captions_from_response(resp)
            except ValueError:
                general_mood = random.choice(DEFAULT_MOODS)
                return self.get_caption(general_mood)

    @init_db
    def get_captions_based_on_author(self, author: str = None) -> list:
        """Get captions from mongo based on author name."""
        resp = Captions.objects(author=author)
        return self.get_captions_from_response(resp)

    @init_db
    def get_users(self, id: str) -> list:
        """Get Users details matching email address."""
        return Users.objects(email=id)

    @init_db
    def create_user(self, **kwargs) -> list:
        """Create User."""
        return Users(**kwargs).save()
