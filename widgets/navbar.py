import streamlit as st

from src import context


class Navbar:  # pylint: disable=too-few-public-methods

    def __init__(self):
        if context.Context.is_logged_in():
            user = context.Context.get_user()
            st.write(user.email)

            if context.Context.project_activated():
                activated_project = context.Context.get_project()
                st.write(f"{activated_project.name} ({activated_project.id_})")
            else:
                st.write('No project selected.')

            refreshed = st.button('Refresh')
            if refreshed:
                st.rerun()

            logged_out = st.button('Logout', on_click=context.Context.logout)
            if logged_out:
                st.rerun()
        else:
            success = context.Context.login()
            if success:
                st.rerun()
