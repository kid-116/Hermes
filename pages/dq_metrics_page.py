import streamlit as st

import constants
from src import rules
from src.context import Context
from src.metrics import TableMetrics
from widgets.disp_metrics import DisplayMetrics
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
    with st.spinner():
        view_tables = rules.load_views(selected_view).items()
        for _, table in view_tables:
            st.dataframe(table.head(constants.DATAFRAME_DISP_SIZE))

            metrics = TableMetrics(table)

            DisplayMetrics(3).render([metrics.get_n_rows()])

            with st.expander('SC - Cardinalities'):
                col_cardinalities = metrics.get_all_column_cardinalities(
                ).items()
                for col_name, col_metrics in col_cardinalities:
                    st.markdown(f'###### {col_name}')
                    DisplayMetrics(5).render(col_metrics)


Page('DQ Metrics',
     dq_metrics_page,
     check_login=True,
     check_active_project=True,
     check_import=True)
