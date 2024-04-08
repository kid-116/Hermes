import os
import subprocess
import tempfile
from typing import Optional
from typing import Sequence

import pandas as pd

import constants
from models.projects import ColumnSchema
from models.projects import ColumnType
from models.projects import Project
from models.projects import ProjectSchema
from models.projects import TableSchema
from models.views import View
from . import utils


def get_tables(_dir: str) -> list[str]:
    files = os.listdir(_dir)
    return [file[:-4] for file in files if file.endswith('.csv')]


def load_table(_dir: str, name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(_dir, name + '.csv'))


def get_columns(df: pd.DataFrame) -> list[str]:
    return list(df.columns)


def load_project_tables(project: Project,
                        schema: Optional[ProjectSchema] = None) -> dict[str, pd.DataFrame]:
    tables = {}
    table_names = get_tables(project.folder)
    for table_name in table_names:
        tables[table_name] = load_table(project.folder, table_name)
    if schema:
        for table_name, table_schema in schema.items():
            for column_name, column_schema in table_schema.items():
                if column_schema.type_ == ColumnType.DATETIME:
                    tables[table_name][column_name] = tables[table_name][column_name].apply(
                        utils.datetime_parser)
    return tables


def transform_view_query(query: str) -> str:
    query = query.strip(';')
    query = query.replace('\n', ' ').replace('[ ]+', ' ').replace('\t', '')
    return query


def load_advanced_view(project: Project, view: View) -> pd.DataFrame:
    assert isinstance(view.rules, str)
    query = transform_view_query(view.rules)
    with tempfile.NamedTemporaryFile(suffix='.csv') as tmpfile:
        assert project.schema
        tables = list(project.schema.keys())
        table_files = [f'{project.folder}/{table}.csv' for table in tables]
        cmd = ['csvsql', '--query', query]
        cmd += table_files
        subprocess.run(cmd, stdout=tmpfile, check=True)
        return pd.read_csv(tmpfile.name)


def check_if_datetime(column: Sequence[str]) -> bool:
    for val in column:
        if not utils.is_datetime(val):
            return False
    return True


def infer_column_type(df: pd.DataFrame, column: str) -> ColumnType:
    match df[column].dtype:
        case 'int64':
            return ColumnType.INTEGER
        case 'float64':
            return ColumnType.FLOAT
        case 'object':
            if check_if_datetime(df[column]):
                return ColumnType.DATETIME
            n_unique = len(df[column].unique())
            if n_unique / len(
                    df
            ) < constants.ENUM_FRACTION_THRESHOLD and n_unique < constants.ENUM_N_THRESHOLD:
                return ColumnType.ENUM
            return ColumnType.STRING
        case _:
            return ColumnType.UNKNOWN


def get_table_schema(df: pd.DataFrame) -> TableSchema:
    schema: TableSchema = {}

    columns = get_columns(df)
    for column in columns:
        type_ = infer_column_type(df, column)
        values: list[str] = []
        has_blanks = None
        is_nullable = bool(df[column].isnull().sum() > 0)
        is_unique = False

        if type_ == ColumnType.ENUM:
            values = list(df[column].unique())

        if type_ in [ColumnType.ENUM, ColumnType.STRING]:
            has_blanks = len(df[df[column] == ''].index) > 0

        if len(df[column].unique()) == len(df):
            is_unique = True

        is_candidate_key = not is_nullable and not has_blanks and is_unique

        schema[column] = ColumnSchema(type_, is_unique, is_candidate_key, is_nullable, has_blanks,
                                      values)

    return schema
