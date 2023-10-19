# todo  the approval list ui is not fitted correctly it should be brought to a unique layout.

from threading import Thread
from firebase_admin import db
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class Index(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            Thread(target=self.fetch_data).run()
        except AttributeError:
            pass

    def fetch_data(self):
        root = db.reference('/').child('to-approve')
        a = root.get()
        for date, user_node in a.items():
            for user, product_node in user_node.items():
                for product_count, product_data in product_node.items():
                    # for key, value in product_data.items():
                    #     print(key, value)
                    # todo check if the current user is the one who has requested for approval and don't add as card as the below code.
                    # if user is not current_user and not product_data['closed']:
                    self.ids.approval_card_holder.add_widget(
                        ApprovalCard(user, product_data['product'], product_data['price']))


class ApprovalCard(BoxLayout):
    username = StringProperty('')
    product = StringProperty('')
    price = StringProperty('')

    def __init__(self, username, product, price):
        super().__init__()
        self.username = username
        self.product = product
        self.price = str(price)
