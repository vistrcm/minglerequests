#!/sbin/venv python


from __future__ import print_function, absolute_import, division
import requests
import logging
import os
import getpass
import ConfigParser
from lxml import etree
from urllib import urlencode

SERVER = 'http://mingle'
API_PATH = '/api/'
API_VER = 'v2'
URL = '{server}{api_path}{api_ver}'.format(
    server=SERVER,
    api_path=API_PATH,
    api_ver=API_VER
)
CONFIG_FILE = os.path.expanduser("~/.mingle_requests")

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)


class Card(object):
    """Representation of mingle card"""

    def __init__(self, mingle, xml):
        # self._number = number
        self.migle = mingle
        self.xml = etree.fromstring(xml)

    def search(self, request):
        """Search for field in card xml."""
        result = self.xml.find(request)
        return result.text

    @property
    def number(self):
        """get card number."""
        logging.debug("trying to search number")
        result = self.search("number")
        return result

    @property
    def name(self):
        """get card name."""
        return self.search("name")

    def __str__(self):
        return "{number}: {name}".format(
            number=self.number,
            name=self.name
        )

    def pretty_xml(self):
        return etree.tostring(self.xml)


class Mingle(object):
    """Representation of mingle"""

    def __init__(self, url, user, password):
        """initialize mingle"""
        self.url = url
        self._api_url = url
        self.user = user
        self.password = password
        self._session = requests.Session()
        self._project = None

    def project():
        doc = "The project property."

        def fget(self):
            logging.debug("getting project")
            return self._project

        def fset(self, value):
            self._project = value
            logging.debug("new project is {}".format(value))
            self.url = "{api}/projects/{project}".format(api=self._api_url,
                                                         project=self._project)

        def fdel(self):
            del self._project
        return locals()

    project = property(**project())

    def card(self, number):
        """Return card."""
        url = "{url}/cards/{number}.xml".format(
            url=self.url,
            number=number)

        logging.debug("GETting url {}".format(url))
        request = self._session.get(url)

        return Card(self, request.text)

    def create_story(self, name):
        """Create card"""
        url = "{url}/cards.xml".format(url=self.url)

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = {'card[name]': name, 'card[card_type_name]': 'story'}

        logging.debug("POSTing url {}".format(url))
        request = self._session.post(
            url,
            data=urlencode(payload),
            headers=headers,
            auth=(self.user, self.password))

        return request.headers['location']


def get_cred():
    """Get credentials from file or user.

    :return: (username, password)"""

    # first try to parse config file
    try:
        logging.debug("getting info from {}".format(CONFIG_FILE))
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)
        username = config.get(SERVER, "username")
        password = config.get(SERVER, "password")
    except Exception, e:
        print("exception on getting data from config: %s" % e)
        print("asking user")
        # get auth info from user
        username = raw_input('input username: ')
        password = getpass.getpass(prompt='input password: ')

    return (username, password)


def main():
    """start programm"""
    username, password = get_cred()

    mingle = Mingle(URL, username, password)
    mingle.project = "devops"
    logging.debug("project is {}".format(mingle.project))

    card = mingle.card(889)
    print(card)
    print(card.pretty_xml())

if __name__ == "__main__":
    main()
