from enum import Enum
import os

import pandas as pd

import constants


class ColumnType(Enum):
    INTEGER = 1, 'INTEGER'
    FLOAT = 2, 'FLOAT'
    STRING = 3, 'STRING'
    ENUM = 4, 'ENUM'
    UNKNOWN = 5, 'UNKNOWN'


def get_tables(_dir):
    files = os.listdir(_dir)
    return [file.strip('.csv') for file in files if file.endswith('.csv')]


def load_table(_dir, name):
    return pd.read_csv(os.path.join(_dir, name + '.csv'))


def get_columns(df):
    return df.columns


def infer_column_type(df, column):
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


def get_schema(df):
    columns = get_columns(df)
    schema = {}
    for column in columns:
        schema[column] = {}

        _type = infer_column_type(df, column)
        schema[column]['type'] = _type

        if _type == ColumnType.ENUM:
            schema[column]['values'] = list(df[column].unique())

        schema[column]['nullable'] = bool(df[column].isnull().sum() > 0)
        if _type in [ColumnType.ENUM, ColumnType.STRING]:
            schema[column]['has_blanks'] = len(df[df[column] == ''].index) > 0

        if len(df[column].unique()) == len(df):
            schema[column]['unique'] = True
        if not schema[column]['nullable'] and not 'has_blanks' in schema[
                column] and 'unique' in schema[column]:
            schema[column]['candidate_key'] = True

        schema[column]['type'] = str(_type.name)

    return schema
