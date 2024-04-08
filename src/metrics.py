import pandas as pd
import seaborn as sns  # type: ignore[import-untyped]

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
            Metric('% Nulls', f'{n_nulls / len(self.df) * 100:.2f} %',
                   'Number of unique values in the column'))

        metrics.append(
            Metric('# Unique', str(len(col.unique())),
                   'Number of unique values in the column'))
        metrics.append(
            Metric('% Unique',
                   f'{len(col.unique()) / len(self.df) * 100:.2f} %',
                   'Percentage of unique values in the column'))

        return metrics

    def get_all_column_cardinalities(self) -> dict[str, list[Metric]]:
        metrics = {}
        for col in self.df.columns:
            metrics[col] = self.get_column_cardinalities(col)
        return metrics

    # pylint: disable=fixme
    # TODO: Compare ColumnType Enum instead of `name` property.
    def is_numeric(self, col_name: str) -> bool:
        return self.schema[col_name].type_.name in ['INTEGER', 'FLOAT']

    # pylint: enable=fixme

    def get_column_distributions(self, col_name: str) -> list[Metric]:
        metrics = []

        col = self.df[col_name]

        is_datetime = self.schema[col_name].type_.name == 'DATETIME'
        is_numeric = self.is_numeric(col_name)
        is_viable = is_datetime or is_numeric

        metrics.append(
            Metric('Min', f'{col.min()}' if is_viable else 'NA',
                   'Minimum value in the column'))
        metrics.append(
            Metric('Max', f'{col.max()}' if is_viable else 'NA',
                   'Maximum value in the column'))

        return metrics

    def get_all_column_distributions(self) -> dict[str, list[Metric]]:
        metrics = {}
        for col in self.df.columns:
            metrics[col] = self.get_column_distributions(col)
        return metrics

    def get_column_hist(self, col_name: str) -> sns.histplot:
        assert self.is_numeric(col_name)
        return sns.histplot(self.df[col_name])
