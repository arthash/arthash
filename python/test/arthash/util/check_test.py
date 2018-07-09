import hashlib, unittest

from arthash.util import check, public_private_key


class CheckTest(unittest.TestCase):
    def test_SHA256(self):
        h = hashlib.sha256()

        for i in range(100):
            check.SHA256.check(h.hexdigest())
            h.update(b'x')

        def check_repetitive(size):
            # Make a string by repeating a segment of CHARS
            mult = 1 + 64 // size
            segment = check.SHA256.CHARS[:size] * mult
            check.SHA256.check(segment[:64])

        for i in range(1, 8):
            with self.assertRaises(ValueError):
                check_repetitive(i)

        for i in range(8, 17):
            check_repetitive(i)

    def test_RSA_public_key(self):
        for i in range(4):
            public, _ = public_private_key.public_private_key()
            check.RSAPublicKey.check(public)
