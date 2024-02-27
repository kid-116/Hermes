import streamlit as st

import constants
from src import auth
from src.firestore import views


def dq_metrics_page():
    st.title('DQ Metrics')

    project = st.session_state.get(constants.ACTIVATE_PROJECT)
    if not project:
        st.error('Please select a project')
        return
    if not project['schema']:
        st.error('Data import is not complete')
        return

    project_views = list(views.get_project_views(project['id']))
    options = [
        f"{view.to_dict()['name']} - {view.id}" for view in project_views
    ]
    selected_view = st.selectbox('Please select a view', options=options)
    _, selected_view_id = selected_view.split(' - ')
    selected_view_doc = [
        view for view in project_views if view.id == selected_view_id
    ][0]

    st.subheader('Rules')
    st.dataframe(selected_view_doc.to_dict()['rules'])


auth.navbar(dq_metrics_page)
