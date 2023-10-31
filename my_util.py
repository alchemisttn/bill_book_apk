from datetime import datetime


def get_username():
    try:
        with open('user', 'r') as f:
            d = eval(f.read())
            return d['username']
    except FileNotFoundError:
        return None


def get_date():
    return datetime.now().strftime("%d-%m-%Y")


history_index_on_behalf = None
