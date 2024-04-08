from __future__ import annotations
from typing import Optional

from firebase_admin import firestore  # type: ignore[import-untyped]
from google.cloud.firestore_v1.base_query import FieldFilter
import pandas as pd

import constants
from .utils import Firestore


class View:

    # pylint: disable=dangerous-default-value
    def __init__(self,
                 id_: str,
                 name: str,
                 project_id: str,
                 rules: dict[str, list[str]] | str = {
                     'column': [],
                     'operator': [],
                     'comparator': [],
                 }):
        self.id_ = id_
        self.name = name
        self.project_id = project_id
        self.rules = rules

    # pylint: enable=dangerous-default-value

    @staticmethod
    def from_doc(doc: firestore.DocumentSnapshot) -> View:
        doc_dict = doc.to_dict()
        return View(doc.id, doc_dict['name'], doc_dict['project_id'], doc_dict['rules'])

    def to_firestore_dict(self) -> dict[str, str | dict[str, list[str]]]:
        return {
            'name': self.name,
            'project_id': self.project_id,
            'rules': self.rules,
        }

    def get_rules_df(self) -> pd.DataFrame:
        assert isinstance(self.rules, dict)
        rules_df = pd.DataFrame(self.rules)
        rules_df = rules_df.astype(str)
        return rules_df

    def is_advanced(self) -> bool:
        return isinstance(self.rules, str)


class ViewDatabase(Firestore):

    def __init__(self) -> None:
        super().__init__('views')

    def add(self, name: str, project_id: str, query: Optional[str] = None) -> None:
        view = View(constants.DEFAULT_MODEL_PLACEHOLDER_ID,
                    name, project_id, query) if query else View(
                        constants.DEFAULT_MODEL_PLACEHOLDER_ID, name, project_id)
        self.col_ref.add(view.to_firestore_dict())

    def get_project_views(self, project_id: str, advanced: Optional[bool] = False) -> list[View]:
        stream = self.col_ref.where(
            filter=FieldFilter('project_id', '==', project_id)  # type: ignore[no-untyped-call]
        ).stream()
        views = [View.from_doc(doc) for doc in stream]
        if advanced is None:
            return views
        if advanced:
            return [view for view in views if isinstance(view.rules, str)]
        return [view for view in views if isinstance(view.rules, dict)]

    def update_rules(self, view: View, rules: pd.DataFrame | str) -> None:
        if isinstance(rules, pd.DataFrame):
            ser_rules: dict[str, list[str]] = {
                str(column): list(values_dict.values())
                for column, values_dict in rules.to_dict().items()
            }
            self.col_ref.document(view.id_).update({'rules': ser_rules})
        else:
            self.col_ref.document(view.id_).update({'rules': rules})
