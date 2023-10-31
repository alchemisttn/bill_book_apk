from kivy.uix.screenmanager import Screen
from firebase_admin import db


class Login(Screen):

    def validator(self):
        local_username = self.ids.username.text
        local_password = self.ids.password.text
        db_root = db.reference('/').child(str(local_username)).child('personal').child('password')
        server_password = db_root.get()
        if not server_password and not db.reference('/').child(str(local_username)).get():
            # info: if there is no password and user present under given user, then create a user and set the typed password.
            # todo: show a popup saying new user created with the given name and password
            # Thread(target=lambda x: db_root.set(local_password)).start()
            # Thread(target=lambda x: db.reference('/').child('user_count').set(
            #     int(db.reference('/').child('user_count').get()) + 1)).start()
            db_root.set(local_password)
            db.reference('/').child('user_count').set(int(db.reference('/').child('user_count').get()) + 1)
            server_password = local_password
        if server_password == local_password:
            # info: if entered password is matching with the server one, then write info to local file and next page
            with open('user', 'x') as f:
                f.write('{"username":"' + str(local_username) + '","password":"' + str(server_password) + '"}')
            self.manager.current = 'index_page'
