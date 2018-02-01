# -*- coding: utf-8 -*-

import os

from nose.tools import eq_, ok_

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
