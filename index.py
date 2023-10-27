# todo  the approval list ui is not fitted correctly it should be brought to a unique layout.

from firebase_admin import db
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from my_util import get_username
from kivymd.uix.button import MDFlatButton


class MyButton(MDFlatButton):
    pass


class Index(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = db.reference('/').child('to-approve')
        self.base_data = None
        self.card_data_holder = []

    def on_pre_enter(self, *args):
        self.base_data = self.root.get()
        self.ids.approval_card_holder.clear_widgets()
        if self.base_data:
            # info: if self.base_data contains data, then add them as cards to the screen
            for date, user_node in self.base_data.items():
                for user, product_node in user_node.items():
                    for product_count, product_data in product_node.items():
                        card_data = {'user': user, 'product': product_data['product'],
                                     'price': product_data['price'], 'date': date, 'product_count': product_count,
                                     'closed': product_data['closed']}
                        if len(card_data) != 0 and not card_data['closed'] and user != get_username():
                            # info: the current user's request-data and closed purchase aren't appended and shown
                            self.card_data_holder.append(card_data)
        for data in self.card_data_holder:
            self.ids.approval_card_holder.add_widget(
                ApprovalCard(data['user'], str(data['product']), data['price'], data['date'], data['product_count'])
            )


class ApprovalCard(BoxLayout):
    username = StringProperty('')
    product = StringProperty('')
    price = StringProperty('')
    button_text = StringProperty('')
    is_approved = BooleanProperty(False)

    def __init__(self, username, product, price, date, product_count):
        super().__init__()
        self.username = username
        self.product = product
        self.price = str(price)
        self.date = date
        self.product_count = product_count
        self.ref = db.reference('/').child('to-approve').child(self.date).child(self.username).child(
            self.product_count)
        self.is_approved = self.ref.child('approvals').child(get_username()).get() or False
        print(self.is_approved)
        self.button_text = 'Approved' if self.is_approved else 'Approve'
        self.is_disabled = not self.is_approved

    def approve_data(self):
        self.ref.child('approvals').child(get_username()).set(True)
        purchase_closed = self.ref.child('closed').get()
        if not purchase_closed:
            # info: check if all have approved and if true then set closed:true
            approvals_dict = {}
            all_user_approvals = self.ref.child('approvals').get()
            if all_user_approvals is not None:
                for users, approvals in all_user_approvals.items():
                    approvals_dict[users] = approvals
            if len(approvals_dict.values()) == int(
                    db.reference('/').child('user_count').get()) and all(approvals_dict.values()):
                # info: if the approved users are same as the count of total users and all have approved then set closed=true
                self.ref.child('closed').set(True)
                purchase_closed = True

        if purchase_closed:
            # note: don't use else, it should be if.
            # info: add the purchase info to the requested user's database.
            path = self.ref.path.split('/')

            data = {}
            for key, value in self.ref.get().items():
                if key not in ['approvals', 'closed']:
                    data[key] = value
            db.reference('/').child(path[3]).child('products').child(path[2]).push().set(data)
        self.disabled = True
