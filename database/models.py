
from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE


connect(db='Go-it_HW8', host="mongodb://localhost:27017")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=100)
    born_location = StringField()
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, required=True, reverse_delete_rule=CASCADE)
    tags = ListField(StringField())
    quote = StringField(required=True)
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
