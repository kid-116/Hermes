from google.cloud.firestore_v1.base_query import FieldFilter

from .utils import Firestore


class User:

    def __init__(self, id_, email):
        self.id_ = id_
        self.email = email

    @staticmethod
    def from_doc(doc):
        doc_dict = doc.to_dict()
        return User(doc.id, doc_dict['email'])

    def to_firestore_dict(self):
        return {'email': self.email}


class UserDatabase(Firestore):

    def __init__(self):
        super().__init__('users')

    def add(self, email):
        user = User(None, email)
        self.col_ref.add(user.to_firestore_dict())
        return self.get(email)

    def get(self, email):
        docs = self.col_ref.where(
            filter=FieldFilter('email', '==', email)).get()
        assert len(docs) <= 1
        if not docs:
            return None
        doc = docs[0]
        return User.from_doc(doc)
