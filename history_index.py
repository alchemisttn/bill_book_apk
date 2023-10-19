from firebase_admin import db
from kivy.uix.screenmanager import Screen

from index import MyButton


class HistoryIndex(Screen):
    def change_page(self, who):
        s = self.manager.get_screen('history_page')
        s.who_from_history_index = who.text
        self.manager.switch_to(s)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = db.reference('/').child('to-approve')
        self.data = self.root.get()

    def on_enter(self, *args):
        user_list = set()
        for date, users in self.data.items():
            for user in users.keys():
                user_list.add(user)
        self.ids.button_holder.add_widget(MyButton(text='All', on_release=self.change_page))
        for name in user_list:
            self.ids.button_holder.add_widget(MyButton(text=name, on_release=self.change_page))
