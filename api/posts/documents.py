from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime


class Post(Document):
    title = StringField(required=True, max_length=255)
    content = StringField(required=True)
    author_id = IntField(required=True)
    created_at = DateTimeField(default=datetime.now)

    meta = {'collection': 'posts'}
