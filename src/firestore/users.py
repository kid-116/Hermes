from google.cloud.firestore_v1 import base_query

from . import utils


class User:

    def __init__(self, email):
        self.email = email

    @staticmethod
    def from_dict(_dict):
        return User(_dict['email'])

    def to_dict(self):
        return {'email': self.email}

    def __repr__(self):
        return str(self.to_dict())

    def __eq__(self, other):
        return self.email == other.email


def get_user(email):
    col = utils.get_collection('users')
    docs = col.where(filter=base_query.FieldFilter('email', '==', email)).get()
    assert len(docs) <= 1
    if len(docs) == 0:
        create_user(email)
        return get_user(email)
    doc = docs[0]
    return doc.id


def create_user(email):
    col = utils.get_collection('users')
    user = User(email)
    col.add(user.to_dict())
