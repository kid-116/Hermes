from typing import Optional

from google.auth.transport import requests  # type: ignore[import-untyped]
from google.oauth2 import id_token  # type: ignore[import-untyped]
import streamlit as st
import streamlit_oauth  # type: ignore[import-untyped]

import constants

google_oauth2 = streamlit_oauth.OAuth2Component(constants.CLIENT_ID, st.secrets.CLIENT_SECRET,
                                                constants.AUTHORIZE_URL, constants.TOKEN_URL,
                                                constants.REFRESH_TOKEN_URL,
                                                constants.REVOKE_TOKEN_URL)


def login() -> Optional[dict[str, str | bool | int]]:
    result = google_oauth2.authorize_button('Login', constants.REDIRECT_URI, constants.SCOPES)
    if result and 'token' in result:
        userinfo: dict[str, str | bool | int] = id_token.verify_oauth2_token(
            result['token']['id_token'], requests.Request(), constants.CLIENT_ID)
        return userinfo

    return None
