from threading import Thread
from firebase_admin import credentials, db

import firebase_admin
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder

from add_product import AddProduct
from bill import Bill
from history import History
from history_index import HistoryIndex
from index import Index
from login import Login


class ScreenHandler(ScreenManager):
    def __init__(self):
        super().__init__()
        Thread(target=connect_server).run()
        try:
            with open('user', 'r') as f:
                if len(f.read()) == 0:
                    self.add_widget(Login(name='login_page'))
                    self.current = 'login_page'
                else:
                    self.add_widget(Index(name='index_page'))
                    self.current = 'index_page'
        except FileNotFoundError:
            self.add_widget(Index(name='index_page'))
            self.current = 'index_page'
        self.add_widget(AddProduct(name='add_product_page'))
        self.current = 'add_product_page'
        self.add_widget(HistoryIndex(name='history_index_page'))
        self.add_widget(History(name='history_page'))
        self.add_widget(Bill(name='bill_page'))


class MyApp_Entrance(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_file('login.kv')  # todo check if user is already logged in and load
        Builder.load_file('index.kv')
        Builder.load_file('add_product.kv')
        Builder.load_file('history_index.kv')
        Builder.load_file('history.kv')
        Builder.load_file('bill.kv')
        return ScreenHandler()


def connect_server():
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ralkz-bill-book-default-rtdb.asia-southeast1.firebasedatabase.app'
    })


MyApp_Entrance().run()
