import streamlit as st

from src.context import Context
from widgets import page


def list_advanced_views() -> None:
    st.subheader('Your Views')

    project = Context.get_project()

    for view in Context.view_db.get_project_views(project.id_, advanced=True):
        st.markdown(f"#### {view.name}")
        st.write(view.id_)

        updated_query = st.text_area('SQL Query', view.rules, key=f'adv-view-query-{view.id_}')

        saved = st.button('Save', key=f'save-view-{view.id_}')
        if saved and updated_query:
            Context.view_db.update_rules(view, updated_query)
            st.success('Rules updated.')


def advanced_view_add_form() -> None:
    st.subheader('Add an Advanced View')

    with st.form('adv_view_add'):
        name = st.text_input('Name')
        query = st.text_area('SQL Query')

        with st.spinner():
            submitted = st.form_submit_button('Add')
        if submitted:
            project = Context.get_project()
            Context.view_db.add(name, project.id_, query)


def advanced_views_page() -> None:
    advanced_view_add_form()
    list_advanced_views()


page.Page('Advanced Views',
          advanced_views_page,
          check_login=True,
          check_active_project=True,
          check_import=True)
