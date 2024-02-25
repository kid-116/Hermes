import streamlit as st

import constants
from src import auth
from src import data_import


def import_page():
    st.title('Data Import')

    project = st.session_state[constants.ACTIVATE_PROJECT]

    clicked = st.button('Run')

    if clicked:
        status = st.status('Processing...', expanded=True)

        status.write('Searching for tables...')
        table_names = data_import.get_tables(project['folder'])

        status.write('Loading tables...')
        table_data = data_import.load_tables(project['folder'], table_names)

        for name in table_names:
            st.subheader(name)
            data_tab, schema_tab = st.tabs(['Data', 'Schema'])
            with data_tab:
                st.dataframe(table_data[name].head(
                    constants.DATAFRAME_DISP_SIZE))
            with schema_tab:
                st.write('Coming soon...')

        status.update(label='Import complete!',
                      state='complete',
                      expanded=False)


auth.navbar(import_page)
