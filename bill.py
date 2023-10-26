from firebase_admin import db
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class HeadingLabel(Label):
    text = StringProperty('')

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text


class BillCard(BoxLayout):
    user_name = StringProperty('')
    user_sum = StringProperty('')

    def __init__(self, text, total, **kwargs):
        super().__init__(**kwargs)
        self.user_name = text
        self.user_sum = str(total)


class Bill(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.full_data = None
        self.users = None
        self.sums = {}
        self.average = None

    def on_pre_enter(self, *args):
        self.full_data = db.reference('/').order_by_key().get()
        if self.full_data:
            for user, user_data in self.full_data.items():
                if user == 'to-approve':
                    return
                self.sums[user] = 0
                for date, product_data in user_data['products'].items():
                    for item_index, item_details in product_data.items():
                        self.sums[user] += int(item_details['price'])

    def on_enter(self, *args):
        self.full_data = db.reference('/').order_by_key().get()
        if self.full_data:
            self.ids.bill_card_holder.add_widget(HeadingLabel('prices'))
            for user, user_data in self.full_data.items():
                if user == 'to-approve':
                    break
                self.sums[user] = 0
                for date, product_data in user_data['products'].items():
                    for item_index, item_details in product_data.items():
                        self.sums[user] += int(item_details['price'])
                self.ids.bill_card_holder.add_widget(BillCard(text=user, total=str(self.sums[user])))
            self.calculate()

    def fetch_data(self):
        pass

    def calculate(self):
        self.ids.bill_card_holder.add_widget(HeadingLabel(' '))
        self.ids.bill_card_holder.add_widget(HeadingLabel(' '))
        self.ids.bill_card_holder.add_widget(HeadingLabel('balance'))
        avg = sum(self.sums.values())/len(self.sums.values())
        for user, personal_price in self.sums.items():
            self.ids.bill_card_holder.add_widget(BillCard(text=user, total=str(avg - self.sums[user])))

