# todo  the approval list ui is not fitted correctly it should be brought to a unique layout.

from firebase_admin import db
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from my_util import get_username
from kivymd.uix.button import MDFlatButton


class MyButton(MDFlatButton):
    pass


class Index(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = db.reference('/').child('to-approve')
        self.a = root.get()

    def on_pre_enter(self, *args):
        if self.a:
            # info: if self.a contains data, then add them as cards to the screen
            for date, user_node in self.a.items():
                for user, product_node in user_node.items():
                    for product_count, product_data in product_node.items():
                        if not any([user == get_username(), product_data['closed']]):
                            self.ids.approval_card_holder.add_widget(
                                ApprovalCard(user, product_data['product'], product_data['price'], date, product_count)
                            )

    def on_enter(self, *args):
        if self.a:
            # info: if self.a contains data, then add them as cards to the screen
            for date, user_node in self.a.items():
                for user, product_node in user_node.items():
                    for product_count, product_data in product_node.items():
                        if not any([user == get_username(), product_data['closed']]):
                            self.ids.approval_card_holder.add_widget(
                                ApprovalCard(user, product_data['product'], product_data['price'], date, product_count)
                            )


class ApprovalCard(BoxLayout):
    username = StringProperty('')
    product = StringProperty('')
    price = StringProperty('')
    button_text = StringProperty('')

    def __init__(self, username, product, price, date, product_count):
        super().__init__()
        self.username = username
        self.product = product
        self.price = str(price)
        self.date = date
        self.product_count = product_count
        self.ref = db.reference('/').child('to-approve').child(self.date).child(self.username).child(
            self.product_count).child('approvals')
        self.button_text = 'Approve' if self.ref.get(get_username()) else 'Approved'

    def approve_data(self):
        if self.button_text == 'Approved':
            self.disabled = True
            return
        self.ref.set({get_username(): 'true'})
