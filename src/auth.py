from google.auth.transport import requests
from google.oauth2 import id_token
import streamlit as st
import streamlit_oauth

import constants
from src.firestore import users

google_oauth2 = streamlit_oauth.OAuth2Component(constants.CLIENT_ID,
                                                st.secrets.CLIENT_SECRET,
                                                constants.AUTHORIZE_URL,
                                                constants.TOKEN_URL,
                                                constants.REFRESH_TOKEN_URL,
                                                constants.REVOKE_TOKEN_URL)


def logout():
    del st.session_state[constants.USER_INFO]
    del st.session_state[constants.ACTIVATE_PROJECT]
    return True


def navbar(page=None):
    if constants.USER_INFO in st.session_state:
        email = st.session_state[constants.USER_INFO]['email']
        st.write(email)

        if constants.ACTIVATE_PROJECT in st.session_state:
            activate_project = st.session_state[constants.ACTIVATE_PROJECT]
            st.write(f"{activate_project['name']} ({activate_project['id']})")
        else:
            st.write('No project selected')

        refreshed = st.button('Refresh')
        if refreshed:
            st.rerun()

        logged_out = st.button('Logout', on_click=logout)
        if logged_out:
            st.rerun()

        active_user = users.get_user(email)
        st.session_state[constants.USER_INFO][constants.USER_ID] = active_user

        if page:
            page()
    else:
        result = google_oauth2.authorize_button('Login', constants.REDIRECT_URI,
                                                constants.SCOPES)
        if result and 'token' in result:
            userinfo = id_token.verify_oauth2_token(result['token']['id_token'],
                                                    requests.Request(),
                                                    constants.CLIENT_ID)
            st.session_state[constants.USER_INFO] = userinfo
            st.rerun()


def is_logged_in(func):

    def inner(*args, **kwargs):
        assert constants.USER_INFO in st.session_state
        return func(*args, **kwargs)

    return inner


@is_logged_in
def get_active_user_id():
    return st.session_state[constants.USER_INFO][constants.USER_ID]
