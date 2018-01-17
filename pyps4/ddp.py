# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 0

DDP_PORT = 987
DDP_VERSION = '00020020'


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

    ps_list = []
    # TODO: maybe more than one PS4 answers in case of broadcast
    data, addr = sock.recvfrom(1024)
    data = parse_ddp_response(data.decode('utf-8'))
    data[u'host-ip'] = addr[0]
    ps_list.append(data)
    return ps_list


def get_status(host):
    """Get status."""
    ps_list = search(host=host)
    return ps_list[0]


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


def launch(host, credential, broadcast=None):
    """Launch."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(5.0)

    if broadcast:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        host = '255.255.255.255'

    msg = get_ddp_launch_message(credential)
    sock.sendto(msg.encode('utf-8'), (host, DDP_PORT))
