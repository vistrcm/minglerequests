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
URL = '{server}{api_path}{api_ver}/'.format(
    server=SERVER,
    api_path=API_PATH,
    api_ver=API_VER
)
CONFIG_FILE = os.path.expanduser("~/.migle_requests")

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

class Mingle:
    """Representation of mingle"""

    def __init__(self, url, user, password):
        """initialize mingle"""
        self.url = url
        self.user = user
        self.password = password
        self._session = requests.Session()
