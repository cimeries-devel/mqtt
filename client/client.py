from paho.mqtt import subscribe
from paho.mqtt import MQTTException
from datetime import datetime
import json


class Client:
    def __init__(self, config):
        self.config = config

    def connect(self):
        try:
            m = subscribe.simple(
                client_id='cimeries',
                topics=['#'],
                hostname='nam1.cloud.thethings.network',
                port=1883,
                auth={'username': self.config.get('user'),
                      'password': self.config.get('pass')},
                msg_count=2)
        except MQTTException:
            return False
        self.payload = m[1]
        return True

    def get_data(self):
        data = json.loads(self.payload.payload.decode())
        message = data.get('uplink_message')
        if not message:
            message = data.get('uplink_normalized')
        d = message['normalized_payload']

        if not isinstance(d, dict):
            d = d[0]
        return self.__serialize(d)

    def is_valid_data(self):
        return not self.payload

    def __serialize(self, data: dict):
        now = datetime.now()
        ec = data.get('soil').get('ec')
        temp = data.get('soil').get('temperature')
        mois = data.get('soil').get('moisture')
        serialize = {
            'battery': data.get('battery'),
            'soil_conductivity': float(ec) if ec else 0,
            'soil_temperature': float(temp) if temp else 0,
            'soil_moisture': float(mois) if mois else 0,
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S')}

        return serialize
