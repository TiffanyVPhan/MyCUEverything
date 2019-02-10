import requests
import re

from time import sleep
from bs4 import BeautifulSoup


class MyCUEverything:
    def __init__(self, _username, _password):
        self.username = _username
        self.password = _password

        self._student_id = None
        self._gpa = None

        self._meal_swipes = None
        self._munch_money = None
        self._campus_cash = None

    def _parse_jsatech(self):
        """ Loads data from colorado.edu/buffonecard """

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

        self._meal_swipes = int(float(soup.find('th', text='Current MP Balance:').parent
                                          .find('th', attrs={'colspan': ''}).get_text()))
        self._munch_money = float(soup.find('th', text='Current MM Balance:').parent
                                      .find('th', attrs={'colspan': ''}).get_text())
        self._campus_cash = float(soup.find('th', text='Current CC Balance:').parent
                                      .find('th', attrs={'colspan': ''}).get_text())

    def _parse_force(self):
        """ Loads data from mycuhub.force.com """

        session = requests.session()

        response = session.get('https://fedauth.colorado.edu/idp/profile/SAML2/Unsolicited/SSO?prov'
                               'iderId=https://CUSalesforceUCBProdStuSvcsCommunity&amp;shire=https:'
                               '//mycuhub.force.com/login?so=00Do0000000Gz4V')

        soup = BeautifulSoup(response.text, 'html.parser')
        action = soup.find('form').get('action')

        payload = {
            'j_username': self.username,
            'j_password': self.password,
            '_eventId_proceed': ''
        }

        response = session.post('https://fedauth.colorado.edu' + action, data=payload)

        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        action = form.get('action')
        saml_response = form.find('input', attrs={'name': 'SAMLResponse'})

        if not saml_response:
            print(soup)

        saml = saml_response.get('value')
        payload = {
            'SAMLResponse': saml
        }

        session.post(action, data=payload)

        response = session.get('https://mycuhub.force.com/apex/adv_StudentView')
        csrf = response.text.split('"ver":42.0,"csrf":"')[1].split('"')[0]
        vid = response.text.split('"vid":"')[1].split('"')[0]
        self._student_id = response.text.split("'adv_StudentView.getTermByTerm'")[1] \
            .split("',")[0] \
            .split("'")[-1]

        payload = f"""{{
            'action': 'adv_StudentView',
            'method': 'getTermByTerm',
            'data': ['{self._student_id}'],
            'type': 'rpc',
            'tid': 2,
            'ctx': {{
                'csrf': '{csrf}',
                'vid': '{vid}',
                'ns': '',
                'ver': 42
            }}
        }}"""

        print(payload)
        response = session.post('https://mycuhub.force.com/apexremote',
                                data=payload,
                                headers={
                                    'Content-Type': 'application/json',
                                    'Referer': 'https://mycuhub.force.com/apex/adv_StudentView'
                                })

        data = response.json()
        print(data)
        try:
            self._gpa = data[0]['result']['careers']['v']['UGRD']['cumlGPA']
        except KeyError:
            self._gpa = 'Bad response from mycuhub.'

    def _parse_portal(self):
        """ Loads data from mycuinfo.colorado.edu """

        session = requests.session()

        response = session.get('https://ping.prod.cu.edu/idp/startSSO.ping?PartnerSpId=SP:Enterpris'
                               'ePortal&IdpSelectorId=BoulderIDP&TargetResource=https://portal.prod'
                               '.cu.edu%2Fpsp%2Fepprod%2FUCB2%2FENTP%2Fh%2F%3Ftab%3DDEFAULT')
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        action = form.get('action')
        saml = form.find('input', attrs={'name': 'SAMLRequest'}).get('value')
        relay = form.find('input', attrs={'name': 'RelayState'}).get('value')

        payload = {
            'SAMLRequest': saml,
            'RelayState': relay
        }

        response = session.post(action, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        action = form.get('action')

        payload = {
            'j_username': self.username,
            'j_password': self.password,
            '_eventId_proceed': 'Log In',
            'timezoneOffset': 0
        }

        response = session.post('https://fedauth.colorado.edu' + action, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        action = form.get('action')
        saml = form.find('input', attrs={'name': 'SAMLResponse'}).get('value')
        relay = form.find('input', attrs={'name': 'RelayState'}).get('value')

        payload = {
            'SAMLResponse': saml,
            'RelayState': relay
        }

        response = session.post(action, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        action = form.get('action')
        saml = form.find('input', attrs={'name': 'SAMLResponse'}).get('value')
        relay = form.find('input', attrs={'name': 'RelayState'}).get('value')

        payload = {
            'SAMLResponse': saml,
            'RelayState': relay
        }

        session.post(action, data=payload)
        session.get('https://portal.prod.cu.edu/psc/epprod/UCB2/ENTP/s/WEBLIB_PTBR.ISCRIPT1.FieldFo'
                    'rmula.IScript_StartPage?HPTYPE=C')

        response = session.get('https://portal.prod.cu.edu/psp/epprod/UCB2/ENTP/h/?cmd=getCachedPgl'
                               't&pageletname=CU_STUDENT_SCHEDULE&tab=CU_STUDENT&PORTALPARAM_COMPWI'
                               'DTH=Narrow&bNoGlobal=Y&ptlayout=N')
        soup = BeautifulSoup(response.text, 'html.parser')
        class_info = soup.find('h3', text='Schedule: Spring 2019')
        class_block = class_info.next_sibling.next_sibling.find('tr').get_text()

        for line in class_block.split('\n'):
            if line:
                classes = re.search(r'\bClasses\b', line)
                if classes:
                    print(line)

    @property
    def student_id(self):
        if self._student_id is None:
            self._parse_force()
        return self._student_id

    @property
    def gpa(self):
        if self._gpa is None:
            self._parse_force()
        return self._gpa

    @property
    def meal_swipes(self):
        if self._meal_swipes is None:
            self._parse_jsatech()
        return self._meal_swipes

    @property
    def munch_money(self):
        if self._munch_money is None:
            self._parse_jsatech()
        return self._munch_money

    @property
    def campus_cash(self):
        if self._campus_cash is None:
            self._parse_jsatech()
        return self._campus_cash
