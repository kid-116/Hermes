from typing import Optional

import streamlit as st

from models.views import View


class ViewSelector:  # pylint: disable=too-few-public-methods

    def __init__(self, views: list[View]):
        self.views = views

    def render(self) -> Optional[View]:
        options = [f"{view.name} - {view.id_}" for view in self.views]
        selected_view_name = st.selectbox('Please select a view', options=options)
        if selected_view_name is None:
            return None
        _, selected_view_id = selected_view_name.split(' - ')
        selected_view = [view for view in self.views if view.id_ == selected_view_id][0]
        return selected_view
