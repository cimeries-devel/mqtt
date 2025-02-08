import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join


class Admin:
    def __init__(self, config, root):
        self.config = config
        self.root = root
        file_key = join(root, config.get('key'))
        self.cred = credentials.Certificate(file_key)
        app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client(app)
        self.lse = self.db.collection('pi').document('lse01')

    def send(self, data: dict):
        self.document = self.db.collection(data['date']).document(data['time'])

        temp_min, temp_max = self.get()

        data['fixed_moisture_min'] = temp_min
        data['fixed_moisture_max'] = temp_max

        self.document.set(data)
        self.lse.set(data)

    def get(self):
        data = self.lse.get()
        if data.exists:
            data = data.to_dict()
            self.config['temperature_min'] = data.get('fixed_moisture_min')
            self.config['temperature_max'] = data.get('fixed_moisture_max')
            self._save_env()

            return data.get('fixed_moisture_min'), \
                data.get('fixed_moisture_max')

        return self.config.get('temperature_min'), \
            self.config.get('temperature_max')

    def _save_env(self):
        with open('{}/.env'.format(self.root), 'w') as f:
            for key, value in self.config.items():
                f.write(f'{key}={value}\n')
