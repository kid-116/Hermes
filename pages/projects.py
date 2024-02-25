import streamlit as st
import streamlit_card

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
                streamlit_card.card(title=doc_dict['name'], text=doc.id)


def projects_page():
    add_project()
    list_projects()


st.title('Projects')

auth.navbar(projects_page)
