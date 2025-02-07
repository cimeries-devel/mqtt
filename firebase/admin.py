import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join


class Admin:
    def __init__(self, config, root):
        file_key = join(root, config.get('key'))
        self.cred = credentials.Certificate(file_key)
        app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client(app)
        self.lse = self.db.collection('pi').document('lse01')

    def send(self, data: dict):
        self.document = self.db.collection(data['date']).document(data['time'])
        self.document.set(data)
        self.lse.set(data)

    def get(self):
        data = self.lse.get()
        if data.exists:
            return data.to_dict()
        return 30
