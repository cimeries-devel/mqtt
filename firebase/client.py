import threading
import firebase_admin
import time
import RPi.GPIO as GPIO
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join


class Pi:
    def __init__(self, config, root):
        self.config = config
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(config.get('pin')), GPIO.OUT)

        file_key = join(root, config.get('key'))
        self.cred = credentials.Certificate(file_key)
        app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client(app)
        self.lse = self.db.collection('pi').document('lse01')
        self.callback_done = threading.Event()

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            data = doc.to_dict()
            sm = data.get('soil_moisture')
            fm = data.get('fixed_moisture')
            self.config['temperature'] = fm
            self._save_env()

            GPIO.output(int(self.config.get('pin')),
                        GPIO.HIGH if sm < fm else GPIO.LOW)

        self.callback_done.set()

    def get(self):
        data = self.lse.get()
        if data.exists:
            return data.to_dict().get('fixed_moisture')
        return None

    def watch(self):
        self.lse.on_snapshot(self.on_snapshot)
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def _save_env(self):
        with open('.env', 'w') as f:
            for key, value in self.config.items():
                f.write(f'{key}={value}\n')

