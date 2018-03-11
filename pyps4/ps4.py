# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging
import time

from .connection import Connection
from .ddp import get_status, launch, wakeup
from .errors import NotReady, UnknownButton

_LOGGER = logging.getLogger(__name__)


def open_credential_file(filename):
    """Open credential file."""
    return json.load(open(filename))


class Ps4(object):
    """The PS4 object."""

    STATUS_OK = 200
    STATUS_STANDBY = 620

    def __init__(self, host, credential=None, credentials_file=None,
                 broadcast=False):
        """Initialize the instance.

        Keyword arguments:
            host -- the host IP address
            credential -- the credential string
            credential_file -- the credendtial file generated with ps4-waker
            broadcast -- use broadcast IP address (default False)
        """
        self._host = host
        self._broadcast = broadcast
        self._socket = None
        self._credential = None
        self._connected = False

        if credential:
            self._credential = credential
        if credentials_file:
            creds = open_credential_file(credentials_file)
            self._credential = creds['user-credential']

        self._connection = Connection(host, credential=self._credential)

    def open(self):
        """Open a connection to the PS4."""
        if self.is_standby():
            raise NotReady

        if not self._connected:
            self.wakeup()
            self.launch()
            time.sleep(0.5)
            self._connection.connect()
            self._connected = True

    def close(self):
        """Close the connection to the PS4."""
        self._connection.disconnect()
        self._connected = False

    def get_status(self):
        """Get current status info.

        Return a dictionary with status information.
        """
        return get_status(self._host)

    def launch(self):
        """Launch."""
        launch(self._host, self._credential)

    def wakeup(self):
        """Wakeup."""
        wakeup(self._host, self._credential)

    def login(self):
        """Login."""
        self.open()
        self._connection.login()
        self.close()

    def standby(self):
        """Standby."""
        self.open()
        self._connection.login()
        self._connection.standby()
        self.close()

    def start_title(self, title_id):
        """Start title.

        `title_id`: title to start
        """
        self.open()
        self._connection.login()
        self._connection.start_title(title_id)
        self.close()

    def remote_control(self, button_name, hold_time=0):
        """ Send a remote control button press.

        Documentation from ps4-waker source:
        near as I can tell, here's how this works:
         - For a simple tap, you send the key with holdTime=0,
           followed by KEY_OFF and holdTime = 0
         - For a long press/hold, you still send the key with
           holdTime=0, the follow it with the key again, but
           specifying holdTime as the hold duration.
         - After sending a direction, you should send KEY_OFF
           to clean it up (since it can just be held forever).
           Doing this after a long-press of PS just breaks it,
           however.
        """
        buttons = []
        buttons.append(button_name)

        self.open()
        self._connection.login()
        self._connection.remote_control(1024, 0)

        for button in buttons:
            try:
                operation = {
                    'up': 1,
                    'down': 2,
                    'right': 4,
                    'left': 8,
                    'enter': 16,
                    'back': 32,
                    'option': 64,
                    'ps': 128,
                    'key_off': 256,
                    'cancel': 512,
                    'open_rc': 1024,
                    'close_rc': 2048,
                }[button.lower()]
            except KeyError:
                raise UnknownButton

            self._connection.remote_control(operation, hold_time)
            self._connection.remote_control(256, 0)
            time.sleep(0.4)

        self._connection.remote_control(2048, 0)
        self.close()

    def get_host_status(self):
        """Get PS4 status code.

        STATUS_OK: 200
        STATUS_STANDBY: 620
        """
        return self.get_status()['status_code']

    def is_running(self):
        """Return if the PS4 is running.

        Returns True or False.
        """
        return True if self.get_host_status() == self.STATUS_OK else False

    def is_standby(self):
        """Return if the PS4 is in standby.

        Returns True or False.
        """
        return True if self.get_host_status() == self.STATUS_STANDBY else False

    def get_system_version(self):
        """Get the system version."""
        return self.get_status()['system-version']

    def get_host_id(self):
        """Get the host id."""
        return self.get_status()['host-id']

    def get_host_name(self):
        """Get the host name."""
        return self.get_status()['host-name']

    def get_running_app_titleid(self):
        """Return the title Id of the running application."""
        return self.get_status()['running-app-titleid']

    def get_running_app_name(self):
        """Return the name of the running application."""
        return self.get_status()['running-app-name']
