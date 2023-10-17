from kivy.uix.screenmanager import Screen
from firebase_admin import db


class Login(Screen):
    auth = False

    def validator(self):
        local_username = self.ids.username.text
        local_password = self.ids.password.text
        db_root = db.reference('/').child(str(local_username)).child('personal').child('password')
        server_password = db_root.get()

        if server_password == local_password:
            self.auth = True
            self.manager.current = 'index_page'
        else:
            pass
