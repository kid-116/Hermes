import streamlit as st

from src.metrics import Metric


class DisplayMetrics:  # pylint: disable=too-few-public-methods

    def __init__(self, n_cols: int = 3) -> None:
        self.n_cols = n_cols

    def render(self, metrics: list[Metric]) -> None:
        cols = st.columns(self.n_cols)
        for idx, metric in enumerate(metrics):
            cols[idx % self.n_cols].metric(label=metric.label,
                                           value=metric.value,
                                           help=metric.help_)
