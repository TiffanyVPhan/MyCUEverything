import requests

from time import sleep
from bs4 import BeautifulSoup


class MyCUEverything:
    def __init__(self, _username, _password):
        self.username = _username
        self.password = _password

        self.meal_swipes = None
        self.munch_money = None
        self.campus_cash = None

    def _parse_jsatech(self):
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

        requests.get(f'https://services.jsatech.com/login.php?skey={skey}' +
                     '&cid=59&fullscreen=1&wason=')

        sleep(4)

        response = requests.get(f'https://services.jsatech.com/index.php?skey={skey}&cid=59&')
        soup = BeautifulSoup(response.text, 'html.parser')

        self.meal_swipes = int(float(soup.find('th', text='Current MP Balance:').parent
                                         .find('th', attrs={'colspan': ''}).get_text()))
        self.munch_money = int(float(soup.find('th', text='Current MM Balance:').parent
                                         .find('th', attrs={'colspan': ''}).get_text()))
        self.campus_cash = int(float(soup.find('th', text='Current CC Balance:').parent
                                         .find('th', attrs={'colspan': ''}).get_text()))

    def get_meal_swipes(self):
        if self.meal_swipes is None:
            self._parse_jsatech()
        return self.meal_swipes

    def get_munch_money(self):
        if self.munch_money is None:
            self._parse_jsatech()
        return self.munch_money

    def get_campus_cash(self):
        if self.campus_cash is None:
            self._parse_jsatech()
        return self.campus_cash
