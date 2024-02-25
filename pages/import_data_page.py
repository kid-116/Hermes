import streamlit as st

import constants
from src import auth
from src import data_import
from src.firestore import projects


def save_schema(project_id, schema):
    projects.save_schema(project_id, schema)
    project = projects.get_project(project_id)
    st.session_state[constants.ACTIVATE_PROJECT] = project


def import_page():
    st.title('Data Import')

    project = st.session_state[constants.ACTIVATE_PROJECT]

    if 'schema' in project:
        for table in project['schema'].keys():
            with st.expander(table):
                st.json(project['schema'][table])

    clicked = st.button('Run' if 'schema' not in project else 'Re-run')

    if clicked:
        status = st.status('Processing...', expanded=True)

        status.write('Searching for tables...')
        table_names = data_import.get_tables(project['folder'])

        status.write('Loading tables...')
        table_data = {}
        for name in table_names:
            table_data[name] = data_import.load_table(project['folder'], name)

        status.write('Infering schema...')
        table_schemas = {}
        for name in table_names:
            table_schemas[name] = data_import.get_schema(table_data[name])

        for name in table_names:
            st.subheader(name)
            data_tab, schema_tab = st.columns([3, 1])
            with data_tab:
                st.markdown('##### Data')
                st.dataframe(
                    table_data[name].head(constants.DATAFRAME_DISP_SIZE),)
            with schema_tab:
                st.markdown('##### Schema')
                schema = table_schemas[name]
                st.json(schema, expanded=False)

        status.update(label='Import complete!',
                      state='complete',
                      expanded=False)

        st.button('Save',
                  on_click=save_schema,
                  args=(project['id'], table_schemas))


def import_page_wrapper():
    if constants.ACTIVATE_PROJECT in st.session_state:
        import_page()
    else:
        st.error('No project selected')


auth.navbar(import_page_wrapper)