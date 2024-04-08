import json
import os

import firebase_admin  # type: ignore[import-untyped]
from firebase_admin import firestore
from firebase_admin import credentials
import streamlit as st

import constants

if os.environ.get('STREAMLIT_USE_CREDENTIALS'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = constants.GOOGLE_APPLICATION_CREDENTIALS


class Firestore:  # pylint: disable=too-few-public-methods

    def __init__(self, col_name: str):

        if not firebase_admin._apps:  # pylint: disable=protected-access
            cred = credentials.Certificate(
                constants.GOOGLE_APPLICATION_CREDENTIALS if os.path.
                isfile('credentials.json') else json.loads(st.secrets.FIRESTORE_CERT))
            firebase_admin.initialize_app(cred)

        db = firestore.Client()  # pylint: disable=no-member
        self.col_ref = db.collection(col_name)
