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

        temp_min, temp_max, average, status = self.get(data)

        data['fixed_moisture_min'] = temp_min
        data['fixed_moisture_max'] = temp_max
        data['average'] = average
        data['status'] = status
        self.document.set(data)
        self.lse.set(data)

    def get(self, data: dict):
        ds = self.lse.get()
        if ds.exists:
            ds = ds.to_dict()
            self.config['temperature_min'] = ds.get('fixed_moisture_min')
            self.config['temperature_max'] = ds.get('fixed_moisture_max')
            self._save_env()

            collection = self.db.collection(data.get('date'))
            docs = collection.get()
            sum = 0
            for doc in docs:
                sum += doc.to_dict().get('soil_moisture')

            average = round(sum/len(docs), 2) if len(docs) != 0 else 0
            status = data.get('soil_moisture') < ds.get('fixed_moisture_min')

            return ds.get('fixed_moisture_min'), \
                ds.get('fixed_moisture_max'), \
                average, status

        return self.config.get('temperature_min'), \
            self.config.get('temperature_max'), \
            0, False

    def _save_env(self):
        with open('{}/.env'.format(self.root), 'w') as f:
            for key, value in self.config.items():
                f.write(f'{key}={value}\n')
