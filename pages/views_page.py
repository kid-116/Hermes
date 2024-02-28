import streamlit as st

from src import rules
from src.context import Context
from widgets import page
from widgets.disp_rules import DisplayRules


def list_views() -> None:
    st.subheader('Your Views')

    project = Context.get_project()

    for view in Context.view_db.get_project_views(project.id_):
        st.markdown(f"#### {view.name}")
        st.write(view.id_)

        edited_rules = DisplayRules(view).render_editable()

        saved = st.button('Save', key=f'save-view-{view.id_}')
        if saved:
            errors = rules.validate(edited_rules, project)

            if not errors:
                Context.view_db.update_rules(view, edited_rules)
                st.success('Rules updated.')
            else:
                for error in errors:
                    st.error(error)


def view_add_form() -> None:
    st.subheader('Add a View')

    with st.form('view_add'):
        name = st.text_input('Name')

        with st.spinner():
            submitted = st.form_submit_button('Add')
        if submitted:
            project = Context.get_project()
            Context.view_db.add(name, project.id_)


def views_page() -> None:
    view_add_form()
    list_views()


page.Page('Views',
          views_page,
          check_login=True,
          check_active_project=True,
          check_import=True)
