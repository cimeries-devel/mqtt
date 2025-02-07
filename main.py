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
            status = client.connect()
            data = client.get_data()
            if status and data:
                admin.send(data)
        except KeyboardInterrupt:
            break
