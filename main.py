from threading import Thread
from firebase_admin import credentials

import firebase_admin
from kivy import Logger
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
        try:
            with open('user', 'r') as f:
                if len(f.read()) == 0:
                    # if there is no data inside the local user auth file open login_page
                    self.add_widget(Login(name='login_page'))
                    self.current = 'login_page'
        except FileNotFoundError:
            self.add_widget(Login(name='login_page'))
            self.current = 'login_page'
        except Exception as ee:
            Logger.error(str(ee))
        self.add_widget(Index(name='index_page'))
        # self.current = 'index_page'
        self.add_widget(AddProduct(name='add_product_page'))
        # self.current = 'add_product_page'
        self.add_widget(HistoryIndex(name='history_index_page'))
        # self.current = 'history_index_page'
        self.add_widget(History(name='history_page'))
        self.add_widget(Bill(name='bill_page'))
        self.current = 'bill_page'


class MyApp_Entrance(MDApp):
    history_index_on_behalf = ''

    def build(self):
        Thread(target=connect_server).run()
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


try:
    MyApp_Entrance().run()
except Exception as e:
    Logger.error(str(e))
