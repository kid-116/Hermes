import streamlit as st

import constants
from src import rules
from src.context import Context
from src.metrics import TableMetrics
from widgets.disp_metrics import DisplayMetrics
from widgets.disp_rules import DisplayRules
from widgets.page import Page
from widgets.view_selector import ViewSelector


def dq_metrics_page() -> None:
    views = Context.view_db.get_project_views(Context.get_project().id_, advanced=False)
    selected_view = ViewSelector(views).render()

    if not selected_view:
        return

    st.subheader('Rules')
    DisplayRules(selected_view).render()

    st.subheader('Filtered Data')
    with st.spinner():
        tables = rules.load_views(selected_view).items()
        for table_name, table in tables:
            st.write(f'##### {table_name}')
            st.dataframe(table.head(constants.DATAFRAME_DISP_SIZE))

            project = Context.get_project()
            assert project.schema
            schema = project.schema[table_name]
            metrics = TableMetrics(table, schema)

            DisplayMetrics(3).render([metrics.get_n_rows()])

            with st.expander('SC - Cardinalities'):
                col_name = st.selectbox(label='Column',
                                        options=table.columns,
                                        key=f'sc-c-col-{table_name}')
                if col_name:
                    col_metrics = metrics.get_column_cardinalities(col_name)
                    DisplayMetrics(5).render(col_metrics)

            with st.expander('SC - Value Distributions'):
                col_name = st.selectbox(label='Column',
                                        options=table.columns,
                                        key=f'sc-d-col-{table_name}')

                if col_name:
                    if metrics.is_numeric(col_name):
                        st.pyplot(metrics.get_column_hist(col_name).figure)
                        st.pyplot(metrics.get_benford_distribution(col_name).figure)

                    col_metrics = metrics.get_column_distributions(col_name)
                    DisplayMetrics(2).render(col_metrics)


Page('DQ Metrics', dq_metrics_page, check_login=True, check_active_project=True, check_import=True)
