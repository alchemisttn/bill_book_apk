from firebase_admin import db
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from my_util import get_username


class Bill(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.full_data = None
        self.users = None
        self.sums = {}
        self.average = None

    def on_pre_enter(self, *args):
        self.full_data = db.reference('/').get()
        for date, user_node in self.a.items():
            for user, product_node in user_node.items():
                for product_count, product_data in product_node.items():
                    if not any([user == get_username(), product_data['closed']]):
                        pass

    def on_enter(self, *args):
        self.full_data = db.reference('/').get()

    def fetch_data(self):
        pass

    def calculate(self, data: list):
        pass

    class HeadingLabel(Label):
        text = StringProperty('')

        def __init__(self, text, **kwargs):
            super().__init__(**kwargs)
            self.text = text
