from firebase_admin import db
from kivy import Logger
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


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
        try:
            self.full_data = db.reference('/').order_by_key().get()
            self.fetch_and_add_data_to_screen()
        except Exception:
            # info: someone has bought nothing
            self.ids.bill_card_holder.add_widget(BillCard(text='total', total=str(sum(self.sums.values()))))

        self.calculate()

    def fetch_and_add_data_to_screen(self):
        if self.full_data:
            self.ids.bill_card_holder.add_widget(HeadingLabel('prices'))
            for user, user_data in self.full_data.items():
                if user == 'to-approve':
                    break
                self.sums[user] = 0
                for date, product_data in user_data['products'].items():
                    print(date, product_data)
                    for item_index, item_details in product_data.items():
                        self.sums[user] += int(item_details['price'])
                self.ids.bill_card_holder.add_widget(BillCard(text=user, total=str(self.sums[user])))
            self.ids.bill_card_holder.add_widget(BillCard(text='total', total=str(sum(self.sums.values()))))

    def calculate(self):
        if len(self.sums.values()) == 0:
            return
        self.ids.bill_card_holder.add_widget(Widget(size_hint_y=None, height=dp(50)))
        self.ids.bill_card_holder.add_widget(HeadingLabel('balance'))
        avg = sum(self.sums.values()) / len(self.sums.values())
        for user, personal_price in self.sums.items():
            self.ids.bill_card_holder.add_widget(BillCard(text=user, total=str(avg - self.sums[user])))
