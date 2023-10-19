from firebase_admin import db
from kivy.uix.screenmanager import Screen

from my_util import get_username, get_date


class AddProduct(Screen):
    def check_out(self):
        if any(map(lambda x: x is None, [self.ids.product.text, self.ids.price.text, self.ids.description.text])):
            return
        ref = db.reference('/').child('to-approve').child(get_date()).child(get_username())
        data = {
            'product': self.ids.product.text,
            'price': self.ids.price.text,
            'description': self.ids.description.text,
            'closed': False,
            'approvals': {get_username(): True}
        }
        ref.push().set(data)
        self.ids.product.text = ''
        self.ids.price.text = ''
        self.ids.description.text = ''


