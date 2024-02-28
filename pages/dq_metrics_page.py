import streamlit as st

import constants
from src import rules
from src.context import Context
from widgets.disp_rules import DisplayRules
from widgets.page import Page


def dq_metrics_page() -> None:
    views = Context.view_db.get_project_views(Context.get_project().id_)
    options = [f"{view.name} - {view.id_}" for view in views]
    selected_view_name = st.selectbox('Please select a view', options=options)
    if selected_view_name is None:
        return
    _, selected_view_id = selected_view_name.split(' - ')
    selected_view = [view for view in views if view.id_ == selected_view_id][0]

    st.subheader('Rules')
    DisplayRules(selected_view).render()

    st.subheader('Filtered Data')
    for _, table in rules.load_views(selected_view).items():
        st.dataframe(table.head(constants.DATAFRAME_DISP_SIZE))


Page('DQ Metrics',
     dq_metrics_page,
     check_login=True,
     check_active_project=True,
     check_import=True)
