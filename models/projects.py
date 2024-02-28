from __future__ import annotations
from typing import Optional

from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore  # type: ignore[import-untyped]

from .utils import Firestore


class Project:

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            id_: Optional[str],
            name: str,
            owner: str,
            folder: str,
            schema: Optional[dict[str, dict[str, str | bool]]] = None) -> None:
        self.id_ = id_
        self.name = name
        self.owner = owner
        self.folder = folder
        self.schema = schema

    # pylint: enable=too-many-arguments

    @staticmethod
    def from_doc(doc: firestore.DocumentSnapshot) -> Project:
        doc_dict = doc.to_dict()
        return Project(doc.id, doc_dict['name'], doc_dict['owner'],
                       doc_dict['folder'], doc_dict['schema'])

    def to_firestore_dict(
            self
    ) -> dict[str, str | Optional[dict[str, dict[str, str | bool]]]]:
        return {
            'name': self.name,
            'owner': self.owner,
            'folder': self.folder,
            'schema': self.schema
        }


class ProjectDatabase(Firestore):

    def __init__(self) -> None:
        super().__init__('projects')

    def add(self, name: str, user_id: str, folder: str) -> Project:
        project = Project(None, name, user_id, folder)
        _, project_ref = self.col_ref.add(project.to_firestore_dict())
        return Project.from_doc(project_ref.get())

    def get_user_projects(self, user_id: str) -> list[Project]:
        stream = self.col_ref.where(filter=FieldFilter(
            'owner', '==', user_id)  # type: ignore[no-untyped-call]
                                   ).stream()
        return [Project.from_doc(doc) for doc in stream]

    def get(self, project_id: str) -> Project:
        doc = self.col_ref.document(project_id).get()
        return Project.from_doc(doc)

    def delete(self, project_id: str) -> None:
        self.col_ref.document(project_id).delete()

    def save_schema(self, project_id: str,
                    schema: dict[str, dict[str, str | bool]]) -> None:
        self.col_ref.document(project_id).update({'schema': schema})
