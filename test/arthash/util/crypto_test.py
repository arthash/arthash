import hashlib, unittest, cryptography.exceptions
from arthash.util import crypto


class CryptoTest(unittest.TestCase):
    def test_works(self):
        public, private = crypto.public_private_key()
        print(public)
        self.assertEqual(len(public), 380)
        self.assertTrue(len(private) > 1670, len(private))
        self.assertTrue(len(private) < 1796, len(private))

    def test_sign_and_verify(self):
        hexdigest = hashlib.sha256().hexdigest()
        private_key = crypto.make_private_key()
        signature = crypto.sign(private_key, hexdigest)
        crypto.verify(private_key, hexdigest, signature)

        # Now change the last byte and see it fail
        sig = bytes.fromhex(signature)
        change = (sig[-1] + 1) % 256
        sig2 = sig[:-1] + bytes([change])
        with self.assertRaises(cryptography.exceptions.InvalidSignature):
            crypto.verify(private_key, hexdigest, crypto.to_hex(sig2))
