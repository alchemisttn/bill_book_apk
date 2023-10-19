from firebase_admin import db
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class HistoryLastSumCard(BoxLayout):
    price = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.price = kwargs['price']


class HistoryCard(BoxLayout):
    date = StringProperty('')
    price = StringProperty('')
    product = StringProperty('')
    username = StringProperty('')

    def __init__(self, date, price, product, username):
        super().__init__()
        self.date = date
        self.price = price
        self.product = product
        self.username = username


class History(Screen):
    who_from_history_index = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = db.reference('/').child('to-approve')
        self.data = self.root.get()

    def on_enter(self, *args):
        total = 0
        for date, users in self.data.items():
            for user, prod_index_data in users.items():
                for prod_index in prod_index_data.values():
                    if self.who_from_history_index == 'All':
                        self.ids.card_holder.add_widget(
                            HistoryCard(date=date, username=user, product=prod_index['product'],
                                        price=prod_index['price']))
                        total += int(prod_index['price'])
                    elif self.who_from_history_index == user:
                        self.ids.card_holder.add_widget(
                            HistoryCard(date=date, username=user, product=prod_index['product'],
                                        price=prod_index['price']))
                        total += int(prod_index['price'])

        self.ids.card_holder.add_widget(HistoryLastSumCard(price=str(total)))
