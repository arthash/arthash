from . import entropy

"""
Check incoming data for format and for randomness.
"""


class Checker:
    PREFIX = ''

    @classmethod
    def check(cls, s):
        if len(s) != cls.LENGTH:
            raise ValueError

        if not s.startswith(cls.PREFIX):
            raise ValueError

        s = s[len(cls.PREFIX):]

        if set(s) - set(cls.CHARS):
            raise ValueError

        if entropy.entropy(s) < cls.MIN_ENTROPY:
            raise ValueError


class RSAPublicKey(Checker):
    PREFIX = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ'
    LENGTH = 380
    MIN_ENTROPY = 5.70
    CHARS = '+/0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


class SHA256(Checker):
    PREFIX = ''
    LENGTH = 64
    MIN_ENTROPY = 3
    CHARS = '0123456789abcdef'
