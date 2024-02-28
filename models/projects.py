from __future__ import annotations
from enum import Enum
from typing import Optional

from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore  # type: ignore[import-untyped]

import constants
from .utils import Firestore


class ColumnType(Enum):
    INTEGER = 1, 'INTEGER'
    FLOAT = 2, 'FLOAT'
    STRING = 3, 'STRING'
    ENUM = 4, 'ENUM'
    UNKNOWN = 5, 'UNKNOWN'


class ColumnSchema:

    # pylint: disable=too-many-arguments
    def __init__(self,
                 type_: ColumnType,
                 is_unique: bool = False,
                 is_candidate_key: bool = False,
                 is_nullable: bool = False,
                 has_blanks: Optional[bool] = False,
                 values: Optional[list[str]] = None):
        self.type_ = type_
        self.is_unique = is_unique
        self.is_candidate_key = is_candidate_key
        self.is_nullable = is_nullable
        self.has_blanks = has_blanks
        self.values: list[str] = values if values else []

    # pylint: enable=too-many-arguments

    @staticmethod
    def from_firestore_dict(
            dict_: dict[str, str | bool | list[str]]) -> ColumnSchema:
        type_ = dict_['type']
        assert isinstance(type_, str)
        is_unique = dict_['is_unique']
        assert isinstance(is_unique, bool)
        is_candidate_key = dict_['is_candidate_key']
        assert isinstance(is_candidate_key, bool)
        is_nullable = dict_['is_nullable']
        assert isinstance(is_nullable, bool)
        has_blanks = dict_['has_blanks']
        assert has_blanks is None or isinstance(has_blanks, bool)
        values = dict_['values']
        assert isinstance(values, list)
        return ColumnSchema(ColumnType[type_], is_unique, is_candidate_key,
                            is_nullable, has_blanks, values)

    def to_firestore_dict(self) -> dict[str, str | bool | list[str] | None]:
        return {
            'type': self.type_.name,
            'is_unique': self.is_unique,
            'is_candidate_key': self.is_candidate_key,
            'is_nullable': self.is_nullable,
            'has_blanks': self.has_blanks,
            'values': self.values
        }

    def __repr__(self) -> str:
        return str(self.to_firestore_dict())


TableSchema = dict[str, ColumnSchema]
ProjectSchema = dict[str, TableSchema]


def project_schema_to_dict(
    schema: ProjectSchema
) -> dict[str, dict[str, dict[str, str | bool | list[str] | None]]]:
    return {
        table_name: {
            column_name: column_schema.to_firestore_dict()
            for column_name, column_schema in table_schema.items()
        } for table_name, table_schema in schema.items()
    }


class Project:

    # pylint: disable=too-many-arguments
    def __init__(self,
                 id_: str,
                 name: str,
                 owner: str,
                 folder: str,
                 schema: Optional[ProjectSchema] = None) -> None:
        self.id_ = id_
        self.name = name
        self.owner = owner
        self.folder = folder
        self.schema = schema

    # pylint: enable=too-many-arguments

    @staticmethod
    def from_doc(doc: firestore.DocumentSnapshot) -> Project:
        doc_dict = doc.to_dict()
        schema = {
            table_name: {
                column_name: ColumnSchema.from_firestore_dict(column_schema)
                for column_name, column_schema in table_schema.items()
            } for table_name, table_schema in doc_dict['schema'].items()
        }
        return Project(doc.id, doc_dict['name'], doc_dict['owner'],
                       doc_dict['folder'], schema)

    def to_firestore_dict(
        self
    ) -> dict[str, str | dict[str, dict[str, dict[str, str | bool | list[str] |
                                                  None]]]]:
        return {
            'name': self.name,
            'owner': self.owner,
            'folder': self.folder,
            'schema': project_schema_to_dict(self.schema)
                      if self.schema else {}
        }


class ProjectDatabase(Firestore):

    def __init__(self) -> None:
        super().__init__('projects')

    def add(self, name: str, user_id: str, folder: str) -> Project:
        project = Project(constants.DEFAULT_MODEL_PLACEHOLDER_ID, name, user_id,
                          folder)
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

    def save_schema(self, project_id: str, schema: ProjectSchema) -> None:
        self.col_ref.document(project_id).update(
            {'schema': project_schema_to_dict(schema)})
