from kivy.uix.screenmanager import Screen
from firebase_admin import db


class Login(Screen):

    def validator(self):
        local_username = self.ids.username.text
        local_password = self.ids.password.text
        db_root = db.reference('/').child(str(local_username)).child('personal').child('password')
        server_password = db_root.get()
        if server_password == local_password:
            self.manager.current = 'index_page'
            with open('user', 'w') as f:
                f.write('{"username":"' + str(local_username) + '","password":"' + str(server_password) + '"}')
            self.manager.current = 'index.kv'
        else:
            return

