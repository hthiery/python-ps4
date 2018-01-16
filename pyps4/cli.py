#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import logging
import pprint

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


def main(args=None):
    """The main function."""
    parser = argparse.ArgumentParser(
        description='PS4 CLI tool.')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='be more verbose')
    parser.add_argument('-H', '--host', type=str, dest='host',
                        help='PS4 IP address', default=None)
    parser.add_argument('-c', '--credential', type=str, dest='credential_file',
                        help='The credential file')
    parser.add_argument('-V', '--version', action='version',
                        version='{version}'.format(version=__version__),
                        help='Print version')

    _sub = parser.add_subparsers(title='Commands')

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

    args = parser.parse_args(args)

    logging.basicConfig()
    if args.verbose:
        logging.getLogger('pyps4').setLevel(logging.DEBUG)

    try:
        playstation = pyps4.Ps4(args.host, args.credential_file)
        playstation.open()
        args.func(playstation, args)
    finally:
        playstation.close()


if __name__ == '__main__':
    main()
