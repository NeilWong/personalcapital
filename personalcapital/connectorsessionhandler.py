import json
import logging

from .client import (
    Client
)
from .exceptions import (
    LoginFailedException
)
from .connector import (
    Connector, 
    RequireTwoFactorException
)

class ConnectorSessionHandler(Connector):
    """
    Extends PersonalCapital to save and load session
    So that it doesn't require 2-factor auth every time
    """
    def __init__(self):
        Connector.__init__(self)
        self.__session_file = 'session.json'
        self.client = Client(self.get_session())

    def start_session(self):
        try:
            self.login()
            self.client.start_client()
        except LoginFailedException:
            raise LoginFailedException('Personal Capital session failed to start')

    def load_session(self):
        try:
            with open(self.__session_file) as data_file:    
                cookies = {}
                try:
                    cookies = json.load(data_file)
                except ValueError as err:
                    logging.error(err)
                self.set_session(cookies)
        except IOError as err:
            logging.error(err)

    def save_session(self):
        with open(self.__session_file, 'w') as data_file:
            data_file.write(json.dumps(self.get_session()))