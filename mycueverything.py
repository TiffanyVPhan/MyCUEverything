import requests

from time import sleep
from bs4 import BeautifulSoup


class MyCUEverything:
    def __init__(self, _username, _password):
        self.username = _username
        self.password = _password

    def get_meal_swipes(self):
        session = requests.session()

        response = session.get('https://services.jsatech.com/login.php?cid=59')
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')

        action = form.get('action')
        skey = form.find(attrs={'name': 'skey'})['value']
        cid = form.find(attrs={'name': 'cid'})['value']

        payload = {
            'save': 1,
            'skey': skey,
            'cid': cid,
            'loginphrase': self.username,
            'password': self.password
        }

        skey = session.post(action, data=payload).text.split("skey=")[1].split("&")[0]

        requests.get(f'https://services.jsatech.com/login.php?skey={skey}&cid=59&fullscreen=1&wason=')

        sleep(4)

        response = requests.get(f'https://services.jsatech.com/index.php?skey={skey}&cid=59&')
        swipes = BeautifulSoup(response.text, 'html.parser') \
            .find('th', text='Current MP Balance:').parent \
            .find('th', attrs={'colspan': ''}).get_text()

        return int(float(swipes))
