from firebase_admin import db
from google.auth.exceptions import TransportError
from kivy.uix.screenmanager import Screen

from index import MyButton


class HistoryIndex(Screen):
    def change_page(self, who):
        s = self.manager.get_screen('history_page')
        s.who_from_history_index = who.text
        self.manager.switch_to(s)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # try:
        self.root = db.reference('/')
        self.data = self.root.get()
        # except TransportError as e:
        #     print(e)

    def on_pre_enter(self, *args):
        self.ids.button_holder.clear_widgets()
        user_list = []
        for user, user_data in self.data.items():
            if user not in ['to-approve', 'user_count']:
                user_list.append(user)
        self.ids.button_holder.add_widget(MyButton(text='All', on_release=self.change_page))
        for name in user_list:
            self.ids.button_holder.add_widget(MyButton(text=name, on_release=self.change_page))
