import streamlit as st

from models.projects import ProjectDatabase
from models.users import UserDatabase
from models.views import ViewDatabase
from . import auth


def check_login(func):

    def inner(*args, **kwargs):
        assert Context.is_logged_in()
        return func(*args, **kwargs)

    return inner


def init_db():
    Context.user_db = UserDatabase()
    Context.project_db = ProjectDatabase()
    Context.view_db = ViewDatabase()


class Context:
    USER = 'user'
    PROJECT = 'project'

    user_db = None
    project_db = None
    view_db = None

    def __init__(self):
        pass

    @staticmethod
    def is_logged_in():
        return Context.USER in st.session_state

    @staticmethod
    def project_activated():
        return Context.PROJECT in st.session_state

    @staticmethod
    def project_import_completed():
        if not Context.project_activated():
            return False
        return bool(st.session_state[Context.PROJECT].schema)

    @staticmethod
    def get_user():
        return st.session_state[Context.USER]

    @staticmethod
    def get_project():
        return st.session_state[Context.PROJECT]

    @staticmethod
    def logout():
        del st.session_state[Context.USER]
        if Context.PROJECT in st.session_state:
            del st.session_state[Context.PROJECT]
        return True

    @staticmethod
    def login():
        userinfo = auth.login()
        if userinfo:
            email = userinfo['email']
            user = Context.user_db.get(email)
            if not user:
                user = Context.user_db.add(email)
            st.session_state[Context.USER] = user

    @staticmethod
    def activate_project(project):
        st.session_state[Context.PROJECT] = project
