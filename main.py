from firebase_admin import credentials, db

import firebase_admin
from google.auth.exceptions import TransportError
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, ScreenManagerException, Screen, FadeTransition, NoTransition
from kivymd.app import MDApp
from kivy.lang import Builder

from add_product import AddProduct
from bill import Bill
from history import History
from history_index import HistoryIndex
from index import Index
from key_json import data
from login import Login


class ScreenHandler(ScreenManager):

    def get_screen(self, name):
        try:
            return super().get_screen(name)
        except ScreenManagerException:
            self.clear_widgets()
            self.add_widget(Index(name='index_page'))
            self.add_widget(AddProduct(name='add_product_page'))
            self.add_widget(HistoryIndex(name='history_index_page'))
            self.add_widget(History(name='history_page'))
            self.current = 'history_index_page'
            self.add_widget(Bill(name='bill_page'))
            self.current = name

    def __init__(self):
        super().__init__()
        self.transition.direction = 'up'
        self.transition.duration = 0.0
        # self.transition = NoTransition()
        self.add_widget(Index(name='index_page'))
        try:
            open('user', 'r')
        except FileNotFoundError:
            self.add_widget(Login(name='login_page'))
            self.current = 'login_page'
            return
        else:
            self.current = 'index_page'
        self.add_widget(AddProduct(name='add_product_page'))
        self.add_widget(HistoryIndex(name='history_index_page'))
        self.add_widget(History(name='history_page'))
        self.add_widget(Bill(name='bill_page'))
        Window.bind(on_keyboard=self.on_back_click)

    def on_back_click(self, window, key, *args):
        if key == 27:
            self.current = App.get_running_app().previous_scrn
            return True


class NoNetwork(Screen):
    pass


class MyApp_Entrance(MDApp):
    history_index_on_behalf = ''
    previous_scrn, stack_scrn = StringProperty('index_page'), []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scrn_manager = None
        self.broad_cast = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        connect_server()
        try:
            # info: check if data is on, else show no_internet page and exit
            db.reference('/').child('user_count').get()
        except TransportError:
            Builder.load_file('no_network.kv')
            Clock.schedule_once(lambda x: exit(), 2)
            return NoNetwork()
        try:
            with open('user', 'r') as f:
                if len(f.read()) != 0:
                    Builder.load_file('login.kv')
        except FileNotFoundError:
            Builder.load_file('login.kv')
        Builder.load_file('index.kv')
        Builder.load_file('add_product.kv')
        Builder.load_file('history_index.kv')
        Builder.load_file('history.kv')
        Builder.load_file('bill.kv')

        try:
            self.scrn_manager = ScreenHandler()
            return self.scrn_manager
        except TransportError:
            Builder.load_file('no_network.kv')
            Clock.schedule_once(lambda x: exit(), 2)
            return NoNetwork()

    def scrn_stack(self, name):
        # info: while leaving the screen, screen-name is added to the stack.
        if name in self.stack_scrn:
            self.stack_scrn.remove(self.previous_scrn)
        self.stack_scrn.append(self.previous_scrn)
        self.previous_scrn = self.stack_scrn.pop()


def connect_server():
    cred = credentials.Certificate(data)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ralkz-bill-book-default-rtdb.asia-southeast1.firebasedatabase.app'
    })


MyApp_Entrance().run()
