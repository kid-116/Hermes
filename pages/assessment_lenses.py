import streamlit as st

import constants
from src.context import Context
from src import data_import
from src import metrics
from widgets.page import Page
from widgets.view_selector import ViewSelector


def assessment_lenses_page() -> None:
    views = Context.view_db.get_project_views(Context.get_project().id_, advanced=True)
    selected_view = ViewSelector(views).render()

    if not selected_view:
        return

    st.text(selected_view.rules)

    with st.spinner('Loading ...'):
        table_df = data_import.load_advanced_view(Context.get_project(), selected_view)
        st.dataframe(table_df.head(constants.DATAFRAME_DISP_SIZE))

        plot_options = ['Boxplot', "Relation"]
        selected_plot = st.selectbox('Please select a plot', options=plot_options)

        numeric_col_names = table_df.select_dtypes(['number']).columns

        match selected_plot:
            case 'Boxplot':
                selected_col = st.selectbox('Please select a column', options=numeric_col_names)

                st.plotly_chart(metrics.get_boxplot(table_df[selected_col]),
                                color=constants.PLOTLY_COLOR)

            case 'Relation':
                x_col = st.selectbox('Select x-axis column', options=numeric_col_names)
                y_col = st.selectbox('Select y-axis column', options=numeric_col_names)

                if x_col and y_col:
                    st.plotly_chart(metrics.get_scatterplot(table_df, x_col, y_col),
                                    color=constants.PLOTLY_COLOR)


Page('Assessment Lenses',
     assessment_lenses_page,
     check_login=True,
     check_active_project=True,
     check_import=True)
