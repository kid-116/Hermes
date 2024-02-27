from google.cloud.firestore_v1.base_query import FieldFilter

from .utils import Firestore


class View:

    def __init__(self, id_, name, project_id, rules=None):
        self.id_ = id_
        self.name = name
        self.project_id = project_id
        self.rules = rules if rules else {
            'column': [],
            'operator': [],
            'comparator': []
        }

    @staticmethod
    def from_doc(doc):
        doc_dict = doc.to_dict()
        return View(doc.id, doc_dict['name'], doc_dict['project_id'],
                    doc_dict['rules'])

    def to_firestore_dict(self):
        return {
            'name': self.name,
            'project_id': self.project_id,
            'rules': self.rules,
        }


class ViewDatabase(Firestore):

    def __init__(self):
        super().__init__('views')

    def add(self, name, project_id):
        view = View(None, name, project_id)
        self.col_ref.add(view.to_firestore_dict())

    def get_project_views(self, project_id):
        stream = self.col_ref.where(
            filter=FieldFilter('project_id', '==', project_id)).stream()
        return [View.from_doc(doc) for doc in stream]

    def update_rules(self, view, rules):
        self.col_ref.document(view.id_).update({'rules': rules})
