# -*- coding: utf-8 -*-

import os

from nose.tools import eq_, ok_
from mock import MagicMock

import pyps4

CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'credentials.json')


class TestPs4(object):

    def test_ps4(self):
        playstation = pyps4.Ps4('10.10.10.10')
        eq_(playstation._host, '10.10.10.10')
        eq_(playstation._broadcast, False)

        playstation = pyps4.Ps4(None, broadcast=True)
        eq_(playstation._host, None)
        eq_(playstation._broadcast, True)

        playstation = pyps4.Ps4('10.10.10.10', credential='abcdef')
        eq_(playstation._credential, 'abcdef')

        playstation = pyps4.Ps4('0.0.0.0', credentials_file=CREDENTIALS_FILE)
        eq_(playstation._credential, '1234567890')

    def test_open_credentials_file(self):
        creds = pyps4.open_credential_file(CREDENTIALS_FILE)

        ok_('client-type' in creds)
        ok_('auth-type' in creds)
        ok_('user-credential' in creds)

    def test_get_host_status(self):
        mock = MagicMock()
        mock.side_effect = [
            {'status_code': 200},
            {'status_code': 620},
        ]

        playstation = pyps4.Ps4('10.10.10.10')
        playstation.get_status = mock
        eq_(playstation.get_host_status(), 200)
        eq_(playstation.get_host_status(), 620)

    def test_is_running(self):
        mock = MagicMock()
        mock.side_effect = [
            {'status_code': 200},
            {'status_code': 620},
            {'status_code': 100},
        ]

        playstation = pyps4.Ps4('10.10.10.10')
        playstation.get_status = mock
        eq_(playstation.is_running(), True)
        eq_(playstation.is_running(), False)
        eq_(playstation.is_running(), False)

    def test_is_standby(self):
        mock = MagicMock()
        mock.side_effect = [
            {'status_code': 620},
            {'status_code': 200},
            {'status_code': 100},
        ]

        playstation = pyps4.Ps4('10.10.10.10')
        playstation.get_status = mock
        eq_(playstation.is_standby(), True)
        eq_(playstation.is_standby(), False)
        eq_(playstation.is_standby(), False)

    def test_get_host_id(self):
        mock = MagicMock()
        mock.side_effect = [
            {'host-id': 'test-A'},
            {'host-name': 'test-B'},
            {'running-app-titleid': 'test-C'},
            {'running-app-name': 'test-D'},
            {'system-version': 'test-E'},
        ]

        playstation = pyps4.Ps4('10.10.10.10')
        playstation.get_status = mock

        eq_(playstation.get_host_id(), 'test-A')
        eq_(playstation.get_host_name(), 'test-B')
        eq_(playstation.get_running_app_titleid(), 'test-C')
        eq_(playstation.get_running_app_name(), 'test-D')
        eq_(playstation.get_system_version(), 'test-E')
