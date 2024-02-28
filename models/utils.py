from firebase_admin import firestore  # type: ignore[import-untyped]


class Firestore:  # pylint: disable=too-few-public-methods

    def __init__(self, col_name: str):
        db = firestore.Client()  # pylint: disable=no-member
        self.col_ref = db.collection(col_name)
