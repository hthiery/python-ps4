# -*- coding: utf-8 -*-
from __future__ import print_function

PUBLIC_KEY = \
    """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxfAO/MDk5ovZpp7xlG9J
JKc4Sg4ztAz+BbOt6Gbhub02tF9bryklpTIyzM0v817pwQ3TCoigpxEcWdTykhDL
cGhAbcp6E7Xh8aHEsqgtQ/c+wY1zIl3fU//uddlB1XuipXthDv6emXsyyU/tJWqc
zy9HCJncLJeYo7MJvf2TE9nnlVm1x4flmD0k1zrvb3MONqoZbKb/TQVuVhBv7SM+
U5PSi3diXIx1Nnj4vQ8clRNUJ5X1tT9XfVmKQS1J513XNZ0uYHYRDzQYujpLWucu
ob7v50wCpUm3iKP1fYCixMP6xFm0jPYz1YQaMV35VkYwc40qgk3av0PDS+1G0dCm
swIDAQAB
-----END PUBLIC KEY-----"""


from Crypto.PublicKey import RSA


def get_public_key():
    key = RSA.importKey(PUBLIC_KEY, passphrase=None)
    publickey = key.publickey()
    print(key)
    print(publickey)
    value = publickey.exportKey(format='DER', pkcs=8)
    return value


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
