#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import logging
import pprint
import sys

import pyps4

try:
    from version import __version__
except ImportError:
    __version__ = 'dev'


_LOGGER = logging.getLogger(__name__)


def cmd_search(_, __):
    """The search command."""
    info = pyps4.search(broadcast=True)
    pprint.pprint(info)


def cmd_status(playstation, _):
    """The status command."""
    info = playstation.get_status()
    pprint.pprint(info)


def cmd_launch(playstation, _):
    """The status command."""
    playstation.launch()


def cmd_wakeup(playstation, _):
    """Wakeup the PS4."""
    playstation.wakeup()


def cmd_login(playstation, _):
    """Login the PS4."""
    try:
        playstation.login()
    except pyps4.NotReady:
        print('playstaion not ready')
        sys.exit(1)


def cmd_standby(playstation, _):
    """Set the PS4 in standby."""
    try:
        playstation.standby()
    except pyps4.NotReady:
        print('playstaion not ready')
        sys.exit(1)


def cmd_start_title(playstation, args):
    """Set the PS4 in standby."""
    try:
        playstation.start_title(args.title_id)
    except pyps4.NotReady:
        print('playstaion not ready')
        sys.exit(1)


def cmd_remote_control(playstation, args):
    """Send a remote control button."""
    try:
        playstation.remote_control(args.button, args.hold_time)
    except pyps4.NotReady:
        print('playstaion not ready')
        sys.exit(1)


def main(args=None):
    """The main function."""
    parser = argparse.ArgumentParser(
        description='PS4 CLI tool.')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='be more verbose')
    parser.add_argument('-H', '--host', type=str, dest='host',
                        help='PS4 IP address', default=None)
    parser.add_argument('-c', '--credential_file', type=str,
                        dest='credential_file', default=None,
                        help='The credential file')
    parser.add_argument('-C', '--credential', type=str,
                        dest='credential', default=None,
                        help='The credential as string')
    parser.add_argument('-V', '--version', action='version',
                        version='{version}'.format(version=__version__),
                        help='Print version')

    _sub = parser.add_subparsers(title='Commands')
    _sub.required = True

    # search all devices
    subparser = _sub.add_parser('search', help='Search for PS4 devices')
    subparser.set_defaults(func=cmd_search)

    # info
    subparser = _sub.add_parser('status', help='Show current status')
    subparser.set_defaults(func=cmd_status)

    # launch
    subparser = _sub.add_parser('launch', help='Show current status')
    subparser.set_defaults(func=cmd_launch)

    # wake
    subparser = _sub.add_parser('wakeup', help='Wakeup the PS4')
    subparser.set_defaults(func=cmd_wakeup)

    # login
    subparser = _sub.add_parser('login', help='Login the PS4')
    subparser.set_defaults(func=cmd_login)

    # standby
    subparser = _sub.add_parser('standby', help='Standby the PS4')
    subparser.set_defaults(func=cmd_standby)

    # start
    subparser = _sub.add_parser('start', help='Start a title')
    subparser.add_argument('title_id', type=str,
                           metavar="TITLE", help='Game title')
    subparser.set_defaults(func=cmd_start_title)

    # remote
    subparser = _sub.add_parser('remote', help='Send remote control')
    subparser.add_argument('button', type=str,
                           metavar="BUTTON", help='button')
    subparser.add_argument('hold_time', type=int, default=0,
                           metavar="HOLD_TIME", help='hold time')
    subparser.set_defaults(func=cmd_remote_control)

    args = parser.parse_args(args)

    playstation = None

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit()

    if args.verbose:
        logging.basicConfig()
        logging.getLogger('pyps4').setLevel(logging.DEBUG)

    try:
        playstation = pyps4.Ps4(args.host, credential=args.credential,
                                credentials_file=args.credential_file)
        args.func(playstation, args)
    finally:
        pass


if __name__ == '__main__':
    main()
