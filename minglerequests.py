#!/sbin/venv python


import requests
import logging
import os
import getpass
import configparser
import xmlhelper
import filehelper
from lxml import etree

SERVER = 'http://mingle'
API_PATH = '/api/'
API_VER = 'v2'
URL = '{server}{api_path}{api_ver}'.format(
    server=SERVER,
    api_path=API_PATH,
    api_ver=API_VER
)
CONFIG_FILE = os.path.expanduser("~/.mingle_requests")
TICKETS_FILE = 'tickets.csv'

logging.basicConfig(
    filename='minglerequests.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

    def card_by_url(self, url):
        """Return card by url"""

        logging.debug("GETting url {}".format(url))
        request = self._session.get(url)

        return Card(self, request.text)

    def card(self, number):
        """Return card."""

        url = "{url}/cards/{number}.xml".format(
            url=self.url,
            number=number)

        return self.card_by_url(url)

    def create_story(self, name, card_properties=None):
        """create card using xml"""
        url = "{url}/cards.xml".format(url=self.url)
        logging.debug("POSTing url {}".format(url))
        headers = {'content-type': 'application/xml'}

        payload = xmlhelper.prepare_card_xml(
            name,
            properties=card_properties)
        logging.debug("xml for card: \n{}".format(payload))

        request = self._session.post(
            url,
            headers=headers,
            data=payload,
            auth=(self.user, self.password))

        logging.debug("request data: {}".format(request.text))
        return request.headers['location']


def get_cred():
    """Get credentials from file or user.

    :return: (username, password)"""

    # first try to parse config file
    try:
        logging.debug("getting info from {}".format(CONFIG_FILE))
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        username = config.get(SERVER, "username")
        password = config.get(SERVER, "password")
    except Exception as e:
        print("exception on getting data from config: %s" % e)
        print("asking user")
        # get auth info from user
        username = input('input username: ')
        password = getpass.getpass(prompt='input password: ')

    return (username, password)


def main():
    """start programm"""
    username, password = get_cred()

    mingle = Mingle(URL, username, password)
    mingle.project = "devops"
    logging.debug("project is {}".format(mingle.project))

    tickets_to_create = filehelper.tickets_from_file(TICKETS_FILE)

    for ticket in tickets_to_create:
        jira_id = ticket['jira_id']
        jira_name = ticket['jira_name']

        card_properties = ticket['properties']

        new_card_url = mingle.create_story(
            "{jira_id} - {jira_name}".format(
                jira_id=jira_id,
                jira_name=jira_name
            ),
            card_properties=card_properties
        )
        logging.info("new card url: {}".format(new_card_url))

        testcard = mingle.card_by_url(new_card_url)

        print(testcard)
        logging.info("created: {}".format(testcard))


if __name__ == "__main__":
    main()
