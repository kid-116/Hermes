from typing import Callable, Optional

import streamlit as st

from src import context
from . import navbar


class Page:  # pylint: disable=too-few-public-methods

    # pylint: disable=too-many-arguments
    def __init__(self,
                 header: str,
                 content: Optional[Callable[[], None]] = None,
                 title: str = 'Hermes',
                 check_login: bool = False,
                 check_active_project: bool = False,
                 check_import: bool = False) -> None:
        st.set_page_config(page_title=title, page_icon=":bar_chart:", layout="wide")

        navbar.Navbar()

        st.title(header)

        if check_login and not context.Context.is_logged_in():
            st.error('You must be logged in to view this page.')
            return

        if check_active_project and not context.Context.project_activated():
            st.error('Please select a project.')
            return

        if check_import and not context.Context.project_import_completed():
            st.error('Please complete data import.')
            return

        if content:
            content()
