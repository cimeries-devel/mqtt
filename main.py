import paho.mqtt.subscribe as subscribe
import json

username = 'app-viviro@ttn'
password = 'NNSXS.KE5A4K2OYBMCX5TKMETGYDLJYKP2X5HA2IWNUHA.SD5MBIPU7W5OI3AXJ44O5WDE5MWS3PW6E5J5TGRKMTZLZGU4QO5Q'
cert = '/home/cimeries/Cimeries/python/mqtt/isrgrootx1.pem'


def connect():
    m = subscribe.simple(client_id='cimeries',
                         topics=['#'],
                         hostname='nam1.cloud.thethings.network',
                         port=1883,
                         auth={'username': username,
                               'password': password},
                         msg_count=2)
    return m[0], m[1]


if __name__ == '__main__':
    while True:
        try:
            topic, payload = connect()
            data = json.loads(str(payload.payload, 'utf-8'))
            message = data['uplink_message']
            payload = message['decoded_payload']
            print(payload)
        except KeyboardInterrupt:
            break
