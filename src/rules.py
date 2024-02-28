import pandas as pd

from models.projects import Project
from models.projects import ColumnType


def validate(rules_df: pd.DataFrame, project: Project) -> list[str]:
    errors = []

    for _, row in rules_df.iterrows():
        (comparator, operator, column) = row
        del operator
        table, column = column.split('.')

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
