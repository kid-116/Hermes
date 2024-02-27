import pandas as pd
import streamlit as st

from widgets import page
from src import rules
from src.context import Context


def list_views():
    st.subheader('Your Views')

    project = Context.get_project()

    columns = [
        f'{table}.{column}' for table in project.schema
        for column in project.schema[table].keys()
    ]

    for view in Context.view_db.get_project_views(project.id_):
        st.markdown(f"#### {view.name}")
        st.write(view.id_)

        rules_df = pd.DataFrame(view.rules)
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
            key=f'view-editor-{view.id_}')

        saved = st.button('Save', key=f'save-view-{view.id_}')
        if saved:
            errors = rules.validate(edited_rules, project)

            if not errors:
                rules_json = edited_rules.to_dict()
                rules_json = {
                    column: list(values_dict.values())
                    for column, values_dict in rules_json.items()
                }
                Context.view_db.update_rules(view, rules_json)
                st.success('Rules updated.')
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
            project = Context.get_project()
            Context.view_db.add(name, project.id_)


def views_page():
    view_add_form()
    list_views()


page.Page('Views',
          views_page,
          check_login=True,
          check_active_project=True,
          check_import=True)
