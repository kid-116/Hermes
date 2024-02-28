import streamlit as st

from src.context import Context
from widgets import page


def dq_metrics_page() -> None:
    views = Context.view_db.get_project_views(Context.get_project().id_)
    options = [f"{view.name} - {view.id_}" for view in views]
    selected_view_name = st.selectbox('Please select a view', options=options)
    if selected_view_name is None:
        return
    _, selected_view_id = selected_view_name.split(' - ')
    selected_view = [view for view in views if view.id_ == selected_view_id][0]

    st.subheader('Rules')
    st.dataframe(selected_view.rules)


page.Page('DQ Metrics',
          dq_metrics_page,
          check_login=True,
          check_active_project=True,
          check_import=True)
