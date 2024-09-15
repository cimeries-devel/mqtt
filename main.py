from client.client import Client
from firebase.admin import Admin
from dotenv import dotenv_values


class App:
    def __init__(self):
        self.config = dotenv_values('.env')


if __name__ == '__main__':
    app = App()
    client = Client(app.config)
    admin = Admin(app.config)

    while True:
        try:
            client.connect()
            if client.is_valid_data():
                break
            admin.send(client.get_data())
        except KeyboardInterrupt:
            break
