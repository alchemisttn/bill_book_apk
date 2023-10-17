from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder

from add_product import AddProduct
from index import Index
from login import Login


class ScreenHandler(ScreenManager):
    def __init__(self):
        super().__init__()
        # self.add_widget(Login(name='login_page'))
        # self.add_widget(Index(name='index_page'))
        self.add_widget(AddProduct(name='add_product'))
        # self.current = 'login_page'
        # self.current = 'index_page'
        self.current = 'add_product'


class MyApp_Entrance(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_file('login.kv')  # todo check if user is already logged in and load
        Builder.load_file('index.kv')
        Builder.load_file('add_product.kv')
        return ScreenHandler()


MyApp_Entrance().run()
