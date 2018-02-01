# -*- coding: utf-8 -*-

from nose.tools import eq_, ok_

import pyps4


class TestPs4(object):

    def test_parse_ddp_response(self):
        response = '''
        HTTP/1.1 200 Ok
        host-id:F8461CE2701E
        host-type:PS4
        host-name:PS4
        host-request-port:997
        device-discovery-protocol-version:00020020
        system-version:05030061'''
        data = pyps4.parse_ddp_response(response)
        eq_(data['status'], 'Ok')
        eq_(data['status_code'], 200)
        eq_(data['host-id'], 'F8461CE2701E')
        eq_(data['host-type'], 'PS4')
        eq_(data['host-name'], 'PS4')
        eq_(data['host-request-port'], '997')
        eq_(data['device-discovery-protocol-version'], '00020020')
        eq_(data['system-version'], '05030061')

        response = '''
        HTTP/1.1 620 Server Standby
        host-id:F8461CE2701E
        host-type:PS4
        host-name:PS4
        host-request-port:997
        device-discovery-protocol-version:00020020
        system-version:05030061'''
        data = pyps4.parse_ddp_response(response)
        eq_(data['status'], 'Server Standby')
        eq_(data['status_code'], 620)

    def test_get_ddp_search_message(self):
        msg = pyps4.get_ddp_search_message()
        ok_(msg.startswith('SRCH * HTTP/1.1\n'))
        ok_('device-discovery-protocol-version:00020020\n' in msg)

    def test_get_ddp_wake_message(self):
        msg = pyps4.get_ddp_wake_message('12345')
        ok_(msg.startswith('WAKEUP * HTTP/1.1\n'))
        ok_('client-type:a\n' in msg)
        ok_('user-credential:12345\n' in msg)
        ok_('auth-type:C\n' in msg)
        ok_('device-discovery-protocol-version:00020020\n' in msg)

    def test_get_ddp_launch_message(self):
        msg = pyps4.get_ddp_launch_message('12345')
        ok_(msg.startswith('LAUNCH * HTTP/1.1\n'))
        ok_('client-type:a\n' in msg)
        ok_('user-credential:12345\n' in msg)
        ok_('auth-type:C\n' in msg)
        ok_('device-discovery-protocol-version:00020020\n' in msg)
