from client.client import Client
from firebase.admin import Admin
from dotenv import dotenv_values
from os.path import dirname, abspath, join


class App:
    def __init__(self):
        self.root = dirname(abspath(__file__))
        config = join(self.root, '.env')
        self.config = dotenv_values(config)


if __name__ == '__main__':
    app = App()
    client = Client(app.config)
    admin = Admin(app.config, app.root)

    while True:
        try:
            client.connect()
            if client.is_valid_data():
                break
            admin.send(client.get_data())
        except KeyboardInterrupt:
            break
