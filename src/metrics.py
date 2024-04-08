from __future__ import annotations
from typing import Any

from benfordslaw import benfordslaw  # type: ignore[import-untyped]
import pandas as pd
import plotly.express as px  # type: ignore[import-untyped]
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
        metrics.append(Metric('# Nulls', str(n_nulls), 'Number of null values in the column'))
        metrics.append(
            Metric('% Nulls', f'{n_nulls / len(self.df) * 100:.2f} %',
                   'Number of unique values in the column'))

        metrics.append(
            Metric('# Unique', str(len(col.unique())), 'Number of unique values in the column'))
        metrics.append(
            Metric('% Unique', f'{len(col.unique()) / len(self.df) * 100:.2f} %',
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

    def get_constancy(self, col: pd.Series[Any]) -> float:
        return float(col.value_counts().max() / len(col))

    def get_benford_distribution(self, col_name: str):  # type: ignore[no-untyped-def]
        assert self.is_numeric(col_name)
        bl = benfordslaw(pos=1)
        bl.fit(self.df[col_name].values)
        return bl.plot()[0]

    def get_column_distributions(self, col_name: str) -> list[Metric]:
        metrics = []

        col = self.df[col_name]

        is_datetime = self.schema[col_name].type_.name == 'DATETIME'
        is_numeric = self.is_numeric(col_name)

        metrics.append(
            Metric('Min', f'{col.min()}' if is_numeric or is_datetime else 'NA',
                   'Minimum value in the column'))
        metrics.append(
            Metric('Max', f'{col.max()}' if is_numeric or is_datetime else 'NA',
                   'Maximum value in the column'))
        metrics.append(
            Metric('Constancy', f'{self.get_constancy(col):.2f}',
                   'Frequency of most frequent element divided by number of rows'))
        metrics.append(
            Metric(
                'Quartiles',
                ', '.join([f'{val:.2f}' for val in list(col.quantile([0.25, 0.5, 0.75]))])
                if is_numeric else 'NA', '3 points that divide the values into 4 equal parts'))

        return metrics

    def get_all_column_distributions(self) -> dict[str, list[Metric]]:
        metrics = {}
        for col in self.df.columns:
            metrics[col] = self.get_column_distributions(col)
        return metrics

    def get_column_hist(self, col_name: str) -> sns.histplot:
        assert self.is_numeric(col_name)
        return sns.histplot(self.df[col_name])


def get_boxplot(col: pd.Series[float | int]) -> sns.boxplot:
    return px.box(y=col)


def get_scatterplot(table_df: pd.DataFrame, x_col: str, y_col: str) -> px.scatter:
    # return sns.scatterplot(x=table_df[x_col], y=table_df[y_col])
    return px.scatter(x=table_df[x_col], y=table_df[y_col])
