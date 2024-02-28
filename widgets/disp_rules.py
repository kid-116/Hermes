import pandas as pd
import streamlit as st

from models.views import View
from src.context import Context


class DisplayRules:  # pylint: disable=too-few-public-methods
    COLUMN_ORDER = ['column', 'operator', 'comparator']

    def __init__(self, view: View) -> None:
        self.view = view

        project = Context.project_db.get(self.view.project_id)
        assert project.schema
        columns = [
            f'{table}.{column}' for table in project.schema
            for column in project.schema[table].keys()
        ]
        self.column_config = {
            'column':
                st.column_config.SelectboxColumn(label='Column',
                                                 options=columns,
                                                 required=True),
            'operator':
                st.column_config.SelectboxColumn(
                    label='Operator',
                    options=['==', '>', '>=', '<', '<=', '!=']),
            'comparator':
                st.column_config.TextColumn(label='Comparator')
        }

    def render_editable(self) -> pd.DataFrame:
        return st.data_editor(self.view.get_rules_df(),
                              column_config=self.column_config,
                              hide_index=True,
                              num_rows='dynamic',
                              column_order=DisplayRules.COLUMN_ORDER,
                              key=f'view-editor-{self.view.id_}')

    def render(self) -> None:
        st.dataframe(
            self.view.get_rules_df(),
            column_config=self.column_config,
            column_order=self.COLUMN_ORDER,
        )
