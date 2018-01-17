# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging

from . import ddp
from .packets import get_public_key

_LOGGER = logging.getLogger(__name__)


def open_credential_file(filename):
    """Open credential file."""
    return json.load(open(filename))


class Ps4(object):
    """The PS4 object."""

    def __init__(self, host, credentials_file=None, broadcast=False):
        """Initialize the instance."""
        self._host = host
        self._broadcast = broadcast
        self._creds = None

        if credentials_file:
            self._creds = open_credential_file(credentials_file)

    def open(self):
        """Open a connection to the PS4."""
        pass

    def close(self):
        """Close the connection to the PS4."""
        pass

    def get_status(self):
        """Get current status info."""
        return ddp.get_status(self._host)

#    def launch(self):
#        """Launch."""
#        ddp.launch(self._host, self._creds['user-credential'])

    def wakeup(self):
        """Wakeup."""
        ddp.wakeup(self._host, self._creds['user-credential'])
