import hashlib, unittest

from arthash.util import public_private_key


class PublicPrivateTest(unittest.TestCase):
    def test_works(self):
        public, private = public_private_key.public_private_key()
        self.assertEqual(len(public), 380)
        self.assertTrue(len(private) > 1700, len(private))
        self.assertTrue(len(private) < 1716, len(private))
