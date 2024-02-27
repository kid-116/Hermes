from firebase_admin import firestore


class Firestore:  # pylint: disable=too-few-public-methods

    def __init__(self, col_name):
        db = firestore.Client()  # pylint: disable=no-member
        self.col_ref = db.collection(col_name)
