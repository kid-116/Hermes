import pandas as pd
import streamlit as st

import constants
from src import auth
from src import rules
from src.firestore import views


def list_views():
    st.subheader('Your Views')

    project = st.session_state[constants.ACTIVATE_PROJECT]

    columns = [
        f'{table}.{column}' for table in project['schema']
        for column in project['schema'][table].keys()
    ]

    for view in views.get_project_views(project['id']):
        view_dict = view.to_dict()
        st.markdown(f"#### {view_dict['name']}")
        st.write(view.id)

        rules_df = pd.DataFrame(view_dict['rules'])
        rules_df = rules_df.astype(str)

        edited_rules = st.data_editor(
            rules_df,
            column_config={
                'column':
                    st.column_config.SelectboxColumn(label='Column',
                                                     options=columns,
                                                     required=True),
                'operator':
                    st.column_config.SelectboxColumn(
                        label='Operator',
                        options=['==', '>', '>=', '<', '<=', '!=']),
                'comparator':
                    st.column_config.TextColumn(label='Comparator')
            },
            hide_index=True,
            num_rows='dynamic',
            column_order=['column', 'operator', 'comparator'],
            key=f'view-editor-{view.id}')

        saved = st.button('Save', key=f'save-view-{view.id}')
        if saved:
            errors = rules.validate(edited_rules, project)

            if not errors:
                rules_json = edited_rules.to_dict()
                rules_json = {
                    column: list(values_dict.values())
                    for column, values_dict in rules_json.items()
                }
                views.update_rules(view.id, rules_json)
            else:
                for error in errors:
                    st.error(error)


def view_add_form():
    st.subheader('Add a View')

    with st.form('view_add'):
        name = st.text_input('Name')

        with st.spinner():
            submitted = st.form_submit_button('Add')
        if submitted:
            project = st.session_state[constants.ACTIVATE_PROJECT]
            views.create_view(name, project['id'])


def views_page():
    st.title('Views')

    project = st.session_state.get(constants.ACTIVATE_PROJECT)
    if not project:
        st.error('Please select a project')
        return
    if not project['schema']:
        st.error('Data import is not complete')
        return

    view_add_form()
    list_views()


auth.navbar(views_page)
