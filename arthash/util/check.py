from . import entropy

"""
Check incoming data for format and for randomness.
"""


class Checker:
    def __init__(self, length, min_entropy, chars, prefix=''):
        self.length = length
        self.min_entropy = min_entropy
        self.chars = chars
        self.prefix = prefix

    def __call__(self, s):
        if len(s) != self.length:
            raise ValueError
        if not s.startswith(self.prefix):
            raise ValueError

        s = s[len(self.prefix):]

        if set(s) - set(self.chars):
            raise ValueError
        if entropy.entropy(s) < self.min_entropy:
            raise ValueError


RSAPublicKey = Checker(
    chars='+/0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
    length=380,
    min_entropy=5.70,
    prefix='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ')


RSASignature = Checker(
    chars='0123456789abcdef',
    length=512,
    min_entropy=3.9)


SHA256 = Checker(
    chars='0123456789abcdef',
    length=64,
    min_entropy=3)
