import streamlit as st
import streamlit_card  # type: ignore[import-untyped]

from src.context import Context
from widgets import page


def add_project() -> None:
    st.subheader('Add a Project')
    csv_tab, sql_tab = st.tabs(['CSV', 'SQL'])

    with csv_tab:
        with st.form('project_add'):
            name = st.text_input('Name')
            folder = st.text_input('Folder')

            with st.spinner():
                submitted = st.form_submit_button('Add')
                if submitted:
                    project = Context.project_db.add(name,
                                                     Context.get_user().id_,
                                                     folder)
                    Context.view_db.add('Base', project.id_)

    with sql_tab:
        st.write('Coming soon...')


def list_projects() -> None:
    st.subheader('Your Projects')
    csv_tab, = st.tabs(['CSV'])

    with csv_tab:
        with st.spinner():
            for project in Context.project_db.get_user_projects(
                    Context.get_user().id_):
                project_tab, actions = st.columns([3, 1])
                with project_tab:
                    project_activated = streamlit_card.card(title=project.name,
                                                            text=project.id_)
                    if project_activated:
                        Context.activate_project(project)
                        st.info(
                            f"Project - {project.name} ({project.id_}) has been activated."
                        )
                with actions:
                    for _ in range(10):
                        st.write('')
                    with st.spinner():
                        st.button('Delete',
                                  on_click=Context.project_db.delete,
                                  args=(project.id_,),
                                  key=f"delete-project-{project.id_}")


def projects_page() -> None:
    add_project()
    list_projects()


page.Page('Projects', content=projects_page, check_login=True)
