from google.cloud.firestore_v1 import base_query

from src import auth
from src.firestore import utils
from . import views


class Project:

    def __init__(self, name, owner, folder, schema=None):
        self.name = name
        self.owner = owner
        self.folder = folder
        self.schema = schema

    @staticmethod
    def from_dict(_dict):
        return Project(_dict['name'], _dict['owner'], _dict['folder'],
                       _dict.get('schema'))

    def to_dict(self):
        return {
            'name': self.name,
            'owner': self.owner,
            'folder': self.folder,
            'schema': self.schema
        }

    def __repr__(self):
        return str(self.to_dict())


@auth.is_logged_in
def create_project(name, folder):
    col = utils.get_collection('projects')
    project = Project(name, auth.get_active_user_id(), folder)
    _, project_ref = col.add(project.to_dict())
    views.create_view('Base', project_ref.id)


@auth.is_logged_in
def get_user_projects():
    col = utils.get_collection('projects')
    return col.where(filter=base_query.FieldFilter(
        'owner', '==', auth.get_active_user_id())).stream()


@auth.is_logged_in
def get_project(project_id):
    col = utils.get_collection('projects')
    doc = col.document(project_id).get()
    assert doc.to_dict()['owner'] == auth.get_active_user_id()
    doc_dict = doc.to_dict()
    doc_dict['id'] = doc.id
    return doc_dict


@auth.is_logged_in
def delete_project(project_id):
    get_project(project_id)
    col = utils.get_collection('projects')
    col.document(project_id).delete()


@auth.is_logged_in
def save_schema(project_id, schema):
    get_project(project_id)
    col = utils.get_collection('projects')
    col.document(project_id).update({'schema': schema})
