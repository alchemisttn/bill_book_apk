from firebase_admin import db
from kivy.uix.screenmanager import Screen

from my_util import get_username, get_date


class AddProduct(Screen):
    def check_out(self):
        ref = db.reference('/').child('to-approve')
        data = {
            'product': self.ids.product,
            'price': self.ids.price,
            'description': self.ids.description,
            'closed': 'false',
            'approvals': {get_username(): 'true'}
        }
        ref.child(get_date()).push().set(data)
