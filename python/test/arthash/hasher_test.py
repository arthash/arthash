import os, unittest

from arthash import hasher

BASE = os.path.dirname(__file__)
DATA_HASH = '9b36b58806fa34131ce330c18a4bb01f73d70413da84c9d3e744e4cf0ea00101'


class HasherTest(unittest.TestCase):
    def test_simple(self):
        h1 = hasher.hasher(os.path.join(BASE, 'data'), 10)
        self.assertEqual(h1, DATA_HASH)

    def test_chunksize(self):
        h0 = hasher.hasher(os.path.join(BASE, 'data'), 4)
        h1 = hasher.hasher(os.path.join(BASE, 'data'), 10)
        self.assertEqual(h0, h1)

    def test_identical(self):
        h0 = hasher.hasher(os.path.join(BASE, 'data'), 4)
        h1 = hasher.hasher(os.path.join(BASE, 'identical_data'), 4)
        self.assertEqual(h0, h1)
        self.assertEqual(h1, DATA_HASH)

    def test_different(self):
        h0 = hasher.hasher(os.path.join(BASE, 'data'), 100)
        h1 = hasher.hasher(os.path.join(BASE, 'different_data'), 100)
        self.assertNotEqual(h0, h1)
