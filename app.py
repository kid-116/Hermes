import os

import firebase_admin
from firebase_admin import credentials
import streamlit as st

import constants
from src import auth

os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = constants.GOOGLE_APPLICATION_CREDENTIALS

logger = st.logger.get_logger(__name__)

if not firebase_admin._apps:  # pylint: disable=protected-access
    cred = credentials.Certificate(constants.GOOGLE_APPLICATION_CREDENTIALS)
    firebase_admin.initialize_app(cred)

st.set_page_config(page_title='Hermes', page_icon=':bar_chart:', layout='wide')

st.title('Hermes')

auth.navbar()
