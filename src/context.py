import streamlit as st

from models.projects import Project
from models.projects import ProjectDatabase
from models.users import User
from models.users import UserDatabase
from models.views import ViewDatabase
from . import auth

# pylint: disable=wrong-spelling-in-comment
# def check_login(func: Callable) -> Callable:

#     def inner(*args, **kwargs):
#         assert Context.is_logged_in()
#         return func(*args, **kwargs)

#     return inner
# pylint: enable=wrong-spelling-in-comment


class Context:
    USER = 'user'
    PROJECT = 'project'

    user_db = UserDatabase()
    project_db = ProjectDatabase()
    view_db = ViewDatabase()

    @staticmethod
    def is_logged_in() -> bool:
        return Context.USER in st.session_state

    @staticmethod
    def project_activated() -> bool:
        return Context.PROJECT in st.session_state

    @staticmethod
    def project_import_completed() -> bool:
        if not Context.project_activated():
            return False
        return bool(st.session_state[Context.PROJECT].schema)

    @staticmethod
    def get_user() -> User:
        user: User = st.session_state[Context.USER]
        return user

    @staticmethod
    def get_project() -> Project:
        project: Project = st.session_state[Context.PROJECT]
        return project

    @staticmethod
    def logout() -> bool:
        del st.session_state[Context.USER]
        if Context.PROJECT in st.session_state:
            del st.session_state[Context.PROJECT]

        return True

    @staticmethod
    def login() -> None:
        userinfo = auth.login()
        if userinfo:
            email = userinfo['email']
            assert isinstance(email, str)
            user = Context.user_db.get(email) if Context.user_db else None
            if not user:
                user = Context.user_db.add(email) if Context.user_db else None
            st.session_state[Context.USER] = user

    @staticmethod
    def activate_project(project: Project) -> None:
        st.session_state[Context.PROJECT] = project
