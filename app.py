from st_pages import show_pages_from_config
import streamlit as st

from widgets import page

logger = st.logger.get_logger(__name__)

show_pages_from_config()

page.Page(header='Hermes')
