import pandas as pd

from models.projects import ColumnType
from models.projects import TableSchema


class Metric:  # pylint: disable=too-few-public-methods

    def __init__(self, label: str, value: str, help_: str) -> None:
        self.label = label
        self.value = value
        self.help_ = help_

    def __repr__(self) -> str:
        return f'{self.label}: {self.value}'


class TableMetrics:

    def __init__(self, df: pd.DataFrame, schema: TableSchema) -> None:
        self.df = df
        self.schema = schema

    def get_n_rows(self) -> Metric:
        return Metric('Rows', str(len(self.df)), 'Number of rows in the table')

    def get_column_cardinalities(self, col_name: str) -> list[Metric]:
        metrics = []

        col = self.df[col_name]

        n_nulls = col.isnull().sum()
        metrics.append(
            Metric('# Nulls', str(n_nulls),
                   'Number of null values in the column'))
        metrics.append(
            Metric('% Nulls', f'{n_nulls / len(self.df):.2f} %',
                   'Number of unique values in the column'))

        metrics.append(
            Metric('# Unique', str(len(col.unique())),
                   'Number of unique values in the column'))
        metrics.append(
            Metric('% Unique', f'{len(col.unique()) / len(self.df):.2f} %',
                   'Percentage of unique values in the column'))

        return metrics

    def get_all_column_cardinalities(self) -> dict[str, list[Metric]]:
        metrics = {}
        for col in self.df.columns:
            metrics[col] = self.get_column_cardinalities(col)
        return metrics

    def get_column_distributions(self, col_name: str) -> list[Metric]:
        metrics = []

        col = self.df[col_name]

        is_numeric = self.schema[col_name].type_ in [
            ColumnType.INTEGER, ColumnType.FLOAT
        ]

        metrics.append(
            Metric('Min',
                   str(col.min()) if is_numeric else 'NA',
                   'Minimum value in the column'))
        metrics.append(
            Metric('Max',
                   str(col.max()) if is_numeric else 'NA',
                   'Maximum value in the column'))

        return metrics

    def get_all_column_distributions(self) -> dict[str, list[Metric]]:
        metrics = {}
        for col in self.df.columns:
            metrics[col] = self.get_column_distributions(col)
        return metrics
