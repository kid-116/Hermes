from google.cloud.firestore_v1 import base_query

from src import auth
from . import utils


class View:

    def __init__(self, name, project_id, rules=None):
        self.name = name
        self.project_id = project_id
        self.rules = rules if rules else {
            'column': [],
            'operator': [],
            'comparator': []
        }

    @staticmethod
    def from_dict(_dict):
        return View(_dict['name'], _dict['project_id'], _dict['rules'])

    def to_dict(self):
        return {
            'name': self.name,
            'project_id': self.project_id,
            'rules': self.rules,
        }

    def __repr__(self):
        return str(self.to_dict())


@auth.is_logged_in
def create_view(name, project_id):
    col = utils.get_collection('views')
    view = View(name, project_id)
    col.add(view.to_dict())


@auth.is_logged_in
def get_project_views(project_id):
    col = utils.get_collection('views')
    return col.where(
        filter=base_query.FieldFilter('project_id', '==', project_id)).stream()
