import requests

from time import sleep
from bs4 import BeautifulSoup


class MyCUEverything:
    def __init__(self, _username, _password):
            self.username = _username
            self.password = _password

            self._meal_swipes = None
            self._munch_money = None
            self._campus_cash = None

    def _parse_portal(self):
            session = requests.session()

            response = session.get('https://ping.prod.cu.edu/idp/startSSO.ping?PartnerSpId=SP:EnterprisePortal&IdpSelectorId=BoulderIDP&TargetResource=https://portal.prod.cu.edu%2Fpsp%2Fepprod%2FUCB2%2FENTP%2Fh%2F%3Ftab%3DDEFAULT')
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            action = form.get('action')
            saml = form.find('input', attrs={'name': 'SAMLRequest'}).get('value')

            payload = {
                'SAMLRequest': saml
            }

            response = session.post(action, data=payload)
            print(response.text)
            payload = {
                'j_username': self.username,
                'j_password': self.password,
                'timezoneOffset': 0,
                '_eventId_proceed': 'Log In'
            }

            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            action = form.get('action')

            response = session.post('https://fedauth.colorado.edu' + action, data=payload)
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            action = form.get('action')
            saml = form.find('input', attrs={'name': 'SAMLResponse'}).get('value')
            payload = {
                'SAMLResponse': saml
            }
            print(payload)