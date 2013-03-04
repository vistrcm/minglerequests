#!/sbin/venv python


from __future__ import print_function, absolute_import, division
import requests
import logging
import os
import getpass
import ConfigParser

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


class Card:
    """Representation of mingle card"""

    def number():
        doc = "The number property."

        def fget(self):
            return self._number

        def fdel(self):
            del self._number
        return locals()
    number = property(**number())

    def __init__(self, mingle, xml):
        # self._number = number
        self.migle = mingle


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

        return request


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


class Test(object):
    """docstring for Test"""

    def __init__(self, arg):
        super(Test, self).__init__()
        self._arg = arg

    def foo():
        doc = "The foo property."

        def fget(self):
            return self._foo

        def fset(self, value):
            logging.debug("new project is {}".format(value))
            self._foo = value
            self._arg = self._arg + self._foo

        def fdel(self):
            del self._foo
        return locals()
    foo = property(**foo())


def main():
    """start programm"""
    username, password = get_cred()

    mingle = Mingle(URL, username, password)
    mingle.project = "devops"
    logging.debug("project is {}".format(mingle.project))

    card = mingle.card(889)
    print(card.text)

if __name__ == "__main__":
    main()
