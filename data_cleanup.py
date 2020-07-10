import json
from ast import literal_eval

import numpy as np
import pandas as pd

import spacy
from app.services.db_services import init_db

"""
This script reads the quotes.csv taken from https://www.kaggle.com/manann/quotes-500k and 
converts "quote, author, category" to "quote, author, main_mood, sub_moods, main_object, sub_objects"
"""


nlp = spacy.load("en_core_web_sm")
SUBJECTS = {"nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"}
OBJECTS = {"dobj", "dative", "attr", "oprd"}
BREAKER_POS = {"CCONJ", "VERB"}
NEGATIONS = {"no", "not", "n't", "never", "none"}


def get_objects(sentence: str) -> list:
    print(sentence)
    doc = nlp(sentence)
    objects = [tok for tok in doc if (tok.dep_ in OBJECTS)]
    return objects


df = pd.read_csv("quotes.csv")

df[["main_mood", "sub_moods"]] = df["category"].str.split(",", n=1, expand=True)

objects = df["caption"].astype(str).apply(get_objects)
df["main_object"] = objects.str[0]
df["sub_objects"] = objects.str[1:]
df = df.drop(columns=["category"])
df = df.applymap(str)
df["sub_objects"] = df["sub_objects"].str.strip("[]")
df["sub_objects"] = df["sub_objects"].str.split(",")
df["sub_objects"] = df.sub_objects.apply(lambda x: literal_eval(str(x)))
df["sub_moods"] = df["sub_moods"].str.split(",")


df = df.replace("", np.nan)
df.sub_moods = df.sub_moods.apply(lambda y: np.nan if len(y) == 0 else y)
df.sub_objects = df.sub_objects.apply(lambda y: np.nan if y == [""] else y)


df.to_csv("new_final.csv", index=False)
df.to_json("new_final.json", orient="records")

# Import json to db
with open("new_final.json") as f:
    file_data = json.load(f)

# Insert in DB
client = init_db()
db = client.caption_maker
db.captions.insert_many(file_data)
client.close()
