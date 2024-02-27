from google.cloud.firestore_v1.base_query import FieldFilter

from .utils import Firestore


class Project:

    def __init__(self, id_, name, owner, folder, schema=None):  # pylint: disable=too-many-arguments
        self.id_ = id_
        self.name = name
        self.owner = owner
        self.folder = folder
        self.schema = schema

    @staticmethod
    def from_doc(doc):
        doc_dict = doc.to_dict()
        return Project(doc.id, doc_dict['name'], doc_dict['owner'],
                       doc_dict['folder'], doc_dict['schema'])

    def to_firestore_dict(self):
        return {
            'name': self.name,
            'owner': self.owner,
            'folder': self.folder,
            'schema': self.schema
        }


class ProjectDatabase(Firestore):

    def __init__(self):
        super().__init__('projects')

    def add(self, name, user_id, folder):
        project = Project(None, name, user_id, folder)
        _, project_ref = self.col_ref.add(project.to_firestore_dict())
        return Project.from_doc(project_ref.get())

    def get_user_projects(self, user_id):
        stream = self.col_ref.where(
            filter=FieldFilter('owner', '==', user_id)).stream()
        return [Project.from_doc(doc) for doc in stream]

    def get(self, project_id):
        doc = self.col_ref.document(project_id).get()
        return Project.from_doc(doc)

    def delete(self, project_id):
        self.col_ref.document(project_id).delete()

    def save_schema(self, project_id, schema):
        self.col_ref.document(project_id).update({'schema': schema})
