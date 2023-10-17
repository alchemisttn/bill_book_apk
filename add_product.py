from firebase_admin import db
from kivy.uix.screenmanager import Screen


class AddProduct(Screen):
    def check_out(self):
        base = db.reference('/').child('to_approve').child('date').child('current_user')
        # get eh product number of rhree=
        # base.push({
        #     'prod-4'':
        #         {
        #             product:name
        #             price:1000
        #             descktiption:'something'
        #             closed:false
        #             approvals:{'rkali':false, 'alchemist'200, 'kartoz':.5}
        #         }
        # })
