from typing import Any, Iterator

import pandas as pd

from models.projects import Project
from models.projects import ColumnType
from models.views import View
from src.context import Context
from . import data_import


def get_rules(rules_df: pd.DataFrame) -> Iterator[tuple[str, str, str, str]]:
    for _, row in rules_df.iterrows():
        (comparator, operator, column) = row
        table, column = column.split('.')
        yield (table, column, operator, comparator)


def validate(rules_df: pd.DataFrame, project: Project) -> list[str]:
    errors = []

    for (table, column, _, comparator) in get_rules(rules_df):
        assert project.schema
        type_ = project.schema[table][column].type_
        try:
            match type_:
                case ColumnType.INTEGER | ColumnType.FLOAT:
                    float(comparator)
                case _:
                    pass
        except:  # pylint: disable=bare-except
            errors.append(
                f'Comparator value ({comparator}) is invalid for column {column} of type {type_}'
            )

    return errors


def load_views(view: View) -> dict[str, pd.DataFrame]:
    project = Context.project_db.get(view.project_id)
    assert project.schema
    tables = data_import.load_project_tables(project)

    for (table, column, operator, comparator) in get_rules(view.get_rules_df()):
        cmp: Any = str(comparator)
        match project.schema[table][column].type_:
            case ColumnType.INTEGER:
                cmp = int(comparator)
            case ColumnType.FLOAT:
                cmp = float(comparator)

        match operator:
            case '==':
                tables[table] = tables[table][tables[table][column] == cmp]
            case '<=':
                tables[table] = tables[table][tables[table][column] <= cmp]
            case '>':
                tables[table] = tables[table][tables[table][column] > cmp]

    return tables
