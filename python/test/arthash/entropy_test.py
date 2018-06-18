import hashlib, unittest

from arthash import entropy


class EntropyTest(unittest.TestCase):
    def test_good(self):
        h = hashlib.sha256()
        for i in range(100):
            entropy.check(h.hexdigest())
            h.update(b'x')

    def test_failures(self):
        chars = '0123456789abcdef'

        def check(size):
            mult = 1 + 64 // size
            segment = chars[:size] * mult
            entropy.check(segment[:64])

        for i in range(1, 8):
            with self.assertRaises(ValueError):
                check(i)

        for i in range(8, 17):
            check(i)