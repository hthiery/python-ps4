# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging

from .ddp import wakeup, get_status

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
        self._credential = None

        if credential:
            self._credential = credential
        if credentials_file:
            creds = open_credential_file(credentials_file)
            self._credential = creds['user-credential']

    def open(self):
        """Open a connection to the PS4."""
        pass

    def close(self):
        """Close the connection to the PS4."""
        pass

    def get_status(self):
        """Get current status info."""
        return get_status(self._host)

#    def launch(self):
#        """Launch."""
#        ddp.launch(self._host, self._credential)

    def wakeup(self):
        """Wakeup."""
        wakeup(self._host, self._credential)
