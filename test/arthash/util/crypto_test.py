import hashlib, unittest

from arthash.util import crypto


class PublicPrivateTest(unittest.TestCase):
    def test_works(self):
        public, private = crypto.public_private_key()
        self.assertEqual(len(public), 380)
        self.assertTrue(len(private) > 1700, len(private))
        self.assertTrue(len(private) < 1716, len(private))
