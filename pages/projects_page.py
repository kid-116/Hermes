import streamlit as st
import streamlit_card

import constants
from src import auth
from src.firestore import projects


def add_project():
    st.subheader('Add a Project')
    csv_tab, sql_tab = st.tabs(['CSV', 'SQL'])

    with csv_tab:
        with st.form('project_add'):
            name = st.text_input('Name')

            with st.spinner():
                submitted = st.form_submit_button('Add')
                if submitted:
                    projects.create_project(name)

    with sql_tab:
        st.write('Coming soon...')


def list_projects():
    st.subheader('Your Projects')
    csv_tab, = st.tabs(['CSV'])

    with csv_tab:
        with st.spinner():
            for doc in projects.get_user_projects():
                doc_dict = doc.to_dict()
                project_name, project_id = doc_dict['name'], doc.id
                project, actions = st.columns([3, 1])
                with project:
                    project_activated = streamlit_card.card(title=project_name,
                                                            text=project_id)
                    if project_activated:
                        st.session_state[constants.ACTIVATE_PROJECT] = {
                            'id': project_id,
                            'name': project_name
                        }
                        st.info(
                            f'Project - {project_name} ({project_id}) has been activated.'
                        )
                with actions:
                    for _ in range(10):
                        st.write('')
                    with st.spinner():
                        st.button('Delete',
                                  on_click=projects.delete_project,
                                  args=(project_id,),
                                  key=f'delete-project-{project_id}')


def projects_page():
    add_project()
    list_projects()


st.title('Projects')

auth.navbar(projects_page)
