from datetime import datetime


def get_username():
    with open('user', 'r') as f:
        d = eval(f.read())
        return d['username']


def get_date():
    print(datetime.now().strftime("%d-%m-%Y"))
