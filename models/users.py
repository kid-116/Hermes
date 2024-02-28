from __future__ import annotations
from typing import Optional

from firebase_admin import firestore  # type: ignore[import-untyped]
from google.cloud.firestore_v1.base_query import FieldFilter

import constants
from .utils import Firestore


class User:

    def __init__(self, id_: str, email: str) -> None:
        self.id_ = id_
        self.email = email

    @staticmethod
    def from_doc(doc: firestore.DocumentSnapshot) -> User:
        doc_dict = doc.to_dict()
        return User(doc.id, doc_dict['email'])

    def to_firestore_dict(self) -> dict[str, str]:
        return {'email': self.email}


class UserDatabase(Firestore):

    def __init__(self) -> None:
        super().__init__('users')

    def add(self, email: str) -> User:
        user = User(constants.DEFAULT_MODEL_PLACEHOLDER_ID, email)
        self.col_ref.add(user.to_firestore_dict())
        added_user = self.get(email)
        assert added_user is not None
        return added_user

    def get(self, email: str) -> Optional[User]:
        docs = self.col_ref.where(filter=FieldFilter(
            'email', '==', email)  # type: ignore[no-untyped-call]
                                 ).get()
        assert len(docs) <= 1
        if not docs:
            return None
        doc = docs[0]
        return User.from_doc(doc)
