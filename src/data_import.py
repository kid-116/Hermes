import os

import pandas as pd

import constants
from models.projects import ColumnSchema
from models.projects import ColumnType
from models.projects import TableSchema


def get_tables(_dir: str) -> list[str]:
    files = os.listdir(_dir)
    return [file.strip('.csv') for file in files if file.endswith('.csv')]


def load_table(_dir: str, name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(_dir, name + '.csv'))


def get_columns(df: pd.DataFrame) -> list[str]:
    return list(df.columns)


def infer_column_type(df: pd.DataFrame, column: str) -> ColumnType:
    match df[column].dtype:
        case 'int64':
            return ColumnType.INTEGER
        case 'float64':
            return ColumnType.FLOAT
        case 'object':
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

        schema[column] = ColumnSchema(type_, is_unique, is_candidate_key,
                                      is_nullable, has_blanks, values)

    return schema
