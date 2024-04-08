import streamlit as st

import constants
from models.projects import ProjectSchema
from models.projects import TableSchema
from src.context import Context
from src import data_import
from widgets import page


def save_schema(project_id: str, schema: ProjectSchema) -> None:
    Context.project_db.save_schema(project_id, schema)
    project = Context.project_db.get(project_id)
    Context.activate_project(project)


def display_schema(schema: TableSchema) -> None:
    schema_json = {
        column_name: column_schema.to_firestore_dict()
        for column_name, column_schema in schema.items()
    }
    st.json(schema_json, expanded=False)


def import_page() -> None:
    project = Context.get_project()

    if project.schema:
        st.subheader('Schema')
        for table in project.schema.keys():
            with st.expander(table):
                display_schema(project.schema[table])

    clicked = st.button('Re-run' if project.schema else 'Run')

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
            table_schemas[name] = data_import.get_table_schema(table_data[name])

        for name in table_names:
            st.subheader(name)
            data_tab, schema_tab = st.columns([3, 1])
            with data_tab:
                st.markdown('##### Data')
                st.dataframe(table_data[name].head(constants.DATAFRAME_DISP_SIZE),)
            with schema_tab:
                st.markdown('##### Schema')
                schema = table_schemas[name]
                display_schema(schema)

        status.update(label='Import complete!', state='complete', expanded=False)

        st.button('Save', on_click=save_schema, args=(project.id_, table_schemas))


page.Page('Data Import', content=import_page, check_login=True, check_active_project=True)
