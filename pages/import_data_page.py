import streamlit as st

import constants
from src.context import Context
from src import data_import
from widgets import page


def save_schema(project_id, schema):
    Context.project_db.save_schema(project_id, schema)
    project = Context.project_db.get(project_id)
    Context.activate_project(project)


def import_page():
    project = Context.get_project()

    schema_exists = project.schema

    if schema_exists:
        for table in project.schema.keys():
            with st.expander(table):
                st.json(project.schema[table])

    clicked = st.button('Re-run' if schema_exists else 'Run')

    if clicked:
        status = st.status('Processing...', expanded=True)

        status.write('Searching for tables...')
        table_names = data_import.get_tables(project.folder)

        status.write('Loading tables...')
        table_data = {}
        for name in table_names:
            table_data[name] = data_import.load_table(project.folder, name)

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
                  args=(project.id_, table_schemas))


page.Page('Data Import',
          content=import_page,
          check_login=True,
          check_active_project=True)
