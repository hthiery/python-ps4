# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging
import time

from .connection import Connection
from .ddp import get_status, launch, wakeup

_LOGGER = logging.getLogger(__name__)


def open_credential_file(filename):
    """Open credential file."""
    return json.load(open(filename))


class Ps4(object):
    """The PS4 object."""

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
        status = self.get_status()
        print(status)
        self.wakeup()
        self.launch()
        time.sleep(0.5)

        if not self._connected:
            self._connection.connect()
            self._connected = True

    def close(self):
        """Close the connection to the PS4."""
        pass

    def get_status(self):
        """Get current status info."""
        return get_status(self._host)

    def get_host_status(self):
        """Get current status."""
        status = get_status(self._host)
        return status['status']

    def launch(self):
        """Launch."""
        launch(self._host, self._credential)

    def wakeup(self):
        """Wakeup."""
        wakeup(self._host, self._credential)

    def login(self):
        if self._connected:
            self._connection.login()

    def standby(self):
        if self._connected:
            self._connection.standby()

    def start_title(self, title_id):
        if self._connected:
            self._connection.start_title(title_id)

    def get_system_version(self):
        """Get the system version."""
        status = self.get_status()
        return status['system-version']

    def get_host_id(self):
        """Get the host id."""
        status = self.get_status()
        return status['host-id']

    def get_host_name(self):
        """Get the host name."""
        status = self.get_status()
        return status['host-name']

    def get_running_app_titleid(self):
        status = self.get_status()
        return status['running-app-titleid']

    def get_running_app_name(self):
        status = self.get_status()
        return status['running-app-name']
