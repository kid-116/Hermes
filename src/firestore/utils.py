from firebase_admin import firestore


def get_db():
    return firestore.Client()  # pylint: disable=no-member


def get_collection(name):
    db = get_db()
    return db.collection(name)
