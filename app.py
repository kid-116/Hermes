import os

import firebase_admin
from firebase_admin import credentials
from st_pages import show_pages_from_config
import streamlit as st

import constants
from widgets import page

os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = constants.GOOGLE_APPLICATION_CREDENTIALS

logger = st.logger.get_logger(__name__)

if not firebase_admin._apps:  # pylint: disable=protected-access
    cred = credentials.Certificate(constants.GOOGLE_APPLICATION_CREDENTIALS)
    firebase_admin.initialize_app(cred)

show_pages_from_config()

page.Page(header='Hermes')
