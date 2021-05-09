import os
import urllib
from dataclasses import dataclass, field

from mongoengine import Document, connect
from mongoengine.fields import (
    IntField,
    ListField,
    StringField,
)
import random
from flask import current_app
from pymongo import MongoClient

DEFAULT_TOPICS: list = [
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

# Quotes limits
NUMBER_OF_QUOTES = 10


class Captions(Document):
    caption = StringField(required=True, max_length=250)
    author = StringField(required=True, max_length=50)
    main_mood = StringField(required=True, max_length=50)
    general_mood = StringField(max_length=50)
    moods = ListField(StringField(max_length=50))
    objects_ = ListField(StringField(max_length=50))
    likes = IntField()


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

    @init_db
    def create_user(self, **kwargs) -> list:
        """Create User."""
        return Users(**kwargs).save()

    def get_quotes_from_response(self, response: Document) -> dict:
        """Get random samples from mongoengine response, returns quotes and keywords."""
        if len(response) >= NUMBER_OF_QUOTES:
            number_of_samples = NUMBER_OF_QUOTES
        else:
            number_of_samples = len(response)
        random_samples = random.sample(set(response), number_of_samples)
        quotes = []
        current_app.logger.info("Final quotes:")
        for sample in random_samples:
            current_app.logger.info(sample.caption)
            quotes.append(sample)
        if not quotes:
            raise ValueError()

        return {"quotes": quotes}

    @init_db
    def get_quotes(
        self, general_mood: str = None, moods: list = None, objects: list = None
    ) -> list:
        """Get captions from mongo based on given parameters."""
        if not general_mood:
            if not moods:
                moods = [random.choice(DEFAULT_TOPICS)]
            if not objects:
                objects = [random.choice(DEFAULT_OBJECTS)]
            resp = Captions.objects(moods__in=moods, objects___in=objects)
            try:
                return self.get_quotes_from_response(resp)
            except ValueError:
                general_mood = random.choice(DEFAULT_TOPICS)
                return self.get_caption(general_mood, objects, moods)

        if moods and objects:
            resp = Captions.objects(
                general_mood=general_mood, moods__in=moods, objects___in=objects
            )
            try:
                return self.get_quotes_from_response(resp)
            except ValueError:
                return self.get_caption(general_mood, objects)

        if moods and not objects:
            resp = Captions.objects(general_mood=general_mood, moods__in=moods)
            try:
                return self.get_quotes_from_response(resp)
            except ValueError:
                return self.get_caption(general_mood)

        if not moods and objects:
            resp = Captions.objects(general_mood=general_mood, objects___in=objects)
            try:
                return self.get_quotes_from_response(resp)
            except ValueError:
                return self.get_caption(general_mood)

        if not moods and not objects:
            resp = Captions.objects(general_mood=general_mood)
            try:
                return self.get_quotes_from_response(resp)
            except ValueError:
                general_mood = random.choice(DEFAULT_TOPICS)
                return self.get_caption(general_mood)

    @init_db
    def get_quotes_based_on_author(self, author: str = None) -> list:
        """Get captions from mongo based on author name."""
        resp = Captions.objects(author=author)
        return self.get_quotes_from_response(resp)

    @init_db
    def get_users(self, email: str) -> list:
        """Get Users details matching email address."""
        return Users.objects(email=email)

    @init_db
    def like_quote(self, id: str) -> int:
        """Increment the like by 1."""
        Captions.objects(id=id).update_one(inc__likes=1)
        likes_count = Captions.objects(id=id)[0].likes

        return likes_count
