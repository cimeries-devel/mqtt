from paho.mqtt import subscribe
from paho.mqtt import MQTTException
from datetime import datetime
import json


class Client:
    def __init__(self, config):
        self.config = config

    def connect(self):
        m = (None, None)
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
            pass
        finally:
            self.payload = m[1]

    def get_data(self):
        data = json.loads(str(self.payload.payload, 'utf-8'))
        message = data['uplink_message']
        d = message['decoded_payload']
        return self.__serialize(d)

    def is_valid_data(self):
        return not self.payload

    def __serialize(self, data: dict):
        now = datetime.now()
        serialize = {'batery': data.get('Bat'),
                     'soil_conductivity': float(data.get('conduct_SOIL')),
                     'soil_temperature': float(data.get('temp_SOIL')),
                     'soil_moisture': float(data.get('water_SOIL')),
                     'date': now.strftime('%Y-%m-%d'),
                     'time': now.strftime('%H:%M:%S')}

        return serialize
