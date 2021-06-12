import os
import urllib
from dataclasses import dataclass, field

from flask_mongoengine import Document
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
NUMBER_OF_QUOTES = 20


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

    def create_user(self, **kwargs) -> list:
        """Create User."""
        return Users(**kwargs).save()

    def get_quotes_from_response(self, response: Document, page: int) -> list:
        """Get random samples from mongoengine response, returns quotes and keywords."""
        current_app.logger.info("Total %s results received, slicing the first %s results.",len(response), NUMBER_OF_QUOTES)
        # response = response[:NUMBER_OF_QUOTES]
        # number_of_samples = len(response)
        # random_samples = random.sample(set(response), number_of_samples)

        paginated_quotes = response.paginate(page=page, per_page=NUMBER_OF_QUOTES)
        current_app.logger.info("Final quotes:")
        for quote in paginated_quotes.items:
            current_app.logger.info("quote: %s",quote.caption)
            current_app.logger.info("topic: %s",quote.general_mood)
            current_app.logger.info("moods: %s",quote.moods)
            current_app.logger.info("objects: %s",quote.objects_)
            current_app.logger.info("likes: %s",quote.likes)
            current_app.logger.info("="*50)
        if not response:
            raise ValueError("Quotes not found.")

        return paginated_quotes

    def get_quotes(
        self, general_mood: str = None, moods: list = None, objects: list = None, order_by_likes: bool = False, page=1
    ) -> list:
        """Get captions from mongo based on given parameters."""
        kwargs = {}
        if general_mood:
            kwargs["general_mood"] = general_mood
        if moods:
            kwargs["moods__in"] = moods
        if objects:
            kwargs["objects___in"] = objects
        
        if not general_mood:
            if not kwargs.get("moods__in"):
                kwargs["moods__in"] = [random.choice(DEFAULT_TOPICS)]

        # Keeping objects in search decreases quality for quotes
        # if not kwargs.get("objects___in"):
        #     kwargs["objects___in"] = [random.choice(DEFAULT_OBJECTS)]

        current_app.logger.info("Parameters to search quotes: %s", kwargs)

        if order_by_likes:
            resp = Captions.objects(**kwargs).order_by('-likes')
        else:
            resp = Captions.objects(**kwargs)

        try:
            return self.get_quotes_from_response(resp,page)
        except ValueError:
            return self.get_quotes(general_mood=random.choice(DEFAULT_TOPICS))

    def get_quotes_based_on_author(self, author: str = None) -> list:
        """Get captions from mongo based on author name."""
        resp = Captions.objects(author=author)
        return self.get_quotes_from_response(resp, page)

    def get_users(self, email: str) -> list:
        """Get Users details matching email address."""
        return Users.objects(email=email)

    def like_quote(self, id: str) -> int:
        """Increment the like by 1."""
        Captions.objects(id=id).update_one(inc__likes=1)
        likes_count = Captions.objects(id=id)[0].likes

        return likes_count
