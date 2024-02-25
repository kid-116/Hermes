from google.cloud.firestore_v1 import base_query

from src import auth
from src.firestore import utils


class Project:

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    @staticmethod
    def from_dict(_dict):
        return Project(_dict['name'], _dict['owner'])

    def to_dict(self):
        return {'name': self.name, 'owner': self.owner}

    def __repr__(self):
        return str(self.to_dict())


@auth.is_logged_in
def create_project(name):
    col = utils.get_collection('projects')
    project = Project(name, auth.get_active_user_id())
    col.add(project.to_dict())


@auth.is_logged_in
def get_user_projects():
    col = utils.get_collection('projects')
    return col.where(filter=base_query.FieldFilter(
        'owner', '==', auth.get_active_user_id())).stream()
