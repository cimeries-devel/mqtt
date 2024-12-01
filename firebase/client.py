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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.get('pin'), GPIO.OUT)
        file_key = join(root, config.get('key'))
        self.cred = credentials.Certificate(file_key)
        app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client(app)
        self.callback_done = threading.Event()

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            batery, date, time, sc, st, sm = doc.to_dict().values()
            GPIO.output(self.config('key'),
                        GPIO.HIGH if sm > 1.5 else GPIO.LOW)

        self.callback_done.set()

    def watch(self):
        ref = self.db.collection('pi').document('lse01')
        ref.on_snapshot(self.on_snapshot)
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def get(self):
        doc = self.db.collection('pi').document('lse01')
        data = doc.get()
        if data.exists:
            print(data.to_dict())
        else:
            print('not data')
