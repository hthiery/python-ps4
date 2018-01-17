# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging
import re
import socket

_LOGGER = logging.getLogger(__name__)

UDP_IP = '0.0.0.0'
UDP_PORT = 0

DDP_PORT = 987
DDP_VERSION = '00020020'
DDP_CLIENT_TYPE = 'vr'
DDP_AUTH_TYPE = 'R'
DDP_MODEL = 'm'
DDP_APP_TYPE = 'r'


def open_credential_file(filename):
    """Open credential file."""
    return json.load(open(filename))


def get_ddp_message(msg_type, data=None):
    """Get DDP message."""
    msg = u'{} * HTTP/1.1\n'.format(msg_type)
    if data:
        for key, value in data.items():
            msg += '{}:{}\n'.format(key, value)
    msg += 'device-discovery-protocol-version:{}\n'.format(DDP_VERSION)
    return msg


def parse_ddp_response(rsp):
    data = {}
    for line in rsp.splitlines():
        re_status = re.compile(r'HTTP/1.1 (?P<code>\d+) (?P<status>.*)')
        line = line.strip()
        # skip empty lines
        if not line:
            continue
        elif re_status.match(line):
            data['status_code'] = re_status.match(line).group('code')
            data['status'] = re_status.match(line).group('status')
        else:
            values = line.split(':')
            data[values[0]] = values[1]
    return data


def get_ddp_search_message():
    """Get DDP search message."""
    return get_ddp_message('SRCH')


def get_ddp_wake_message(credential):
    """Get DDP wake message."""
    data = {
        'user-credential': credential,
        'client-type': 'a',
        'auth-type': 'C',
    }
    return get_ddp_message('WAKEUP', data)


def get_ddp_launch_message(credential):
    """Get DDP launch message."""
    data = {
        'user-credential': credential,
        'client-type': 'a',
        'auth-type': 'C',
    }
    return get_ddp_message('LAUNCH', data)


def search(host=None, broadcast=True):
    """Discover PS4s."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(5.0)

    if broadcast:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        host = '255.255.255.255'

    msg = get_ddp_search_message()
    sock.sendto(msg.encode('utf-8'), (host, DDP_PORT))
    data, addr = sock.recvfrom(1024)
    data = parse_ddp_response(data.decode('utf-8'))
    data['host-ip'] = addr[0]
    return data


def wakeup(host, credential, broadcast=None):
    """Wakeup PS4s."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(5.0)

    if broadcast:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        host = '255.255.255.255'

    msg = get_ddp_wake_message(credential)
    sock.sendto(msg.encode('utf-8'), (host, DDP_PORT))


#def launch(host, credential, broadcast=None):
#    """Launch."""
#    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    sock.bind((UDP_IP, UDP_PORT))
#    sock.settimeout(5.0)
#
#    if broadcast:
#        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#        host = '255.255.255.255'
#
#    data = {
#        'user-credential': credential,
#    }
#    msg = get_ddp_message('WAKEUP', data)
#    sock.sendto(msg, (host, DDP_PORT))
#
#    #msg = get_ddp_launch_message(credential)
#    msg = get_ddp_message('LAUNCH', data)
#    sock.sendto(msg, (host, DDP_PORT))


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
        return search(self._host)

#    def launch(self):
#        """Launch."""
#        launch(self._host, self._creds['user-credential'])

    def wakeup(self):
        """Wakeup."""
        wakeup(self._host, self._creds['user-credential'])


class Packet(object):
    """The package object."""

    def __init__(self):
        """Initialize the instance."""
        self._length = 0

    def encrypt(self):
        """Encrypt the packet."""
        pass

    def decrypt(self):
        """Encrypt the packet."""
        pass
