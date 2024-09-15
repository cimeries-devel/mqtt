import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Admin:
    def __init__(self, config):
        self.cred = credentials.Certificate(config.get('key'))
        app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client(app)

    def send(self, data: dict):
        self.document = self.db.collection(data['date']).document(data['time'])
        self.document.set(data)
