from firebase.client import Pi
from dotenv import dotenv_values
from os.path import dirname, abspath, join


class App:
    def __init__(self):
        self.root = dirname(abspath(__file__))
        config = join(self.root, '.env')
        self.config = dotenv_values(config)


if __name__ == '__main__':
    app = App()
    pi = Pi(app.config, app.root)
    pi.watch()
