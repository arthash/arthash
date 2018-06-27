import hashlib, os, unittest
from arthash import hasher
from unittest import mock

BASE = os.path.dirname(__file__)
DATA_HASH = 'a7628a45fa12cfa8859e8bd7ceb8b2b399e85557e2c6b9b2a93351044285dc20'


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
        h1 = hasher.hasher(os.path.join(BASE, 'identical_data', 'data'), 4)
        self.assertEqual(h0, h1)
        self.assertEqual(h1, DATA_HASH)

    def test_different(self):
        h0 = hasher.hasher(os.path.join(BASE, 'data'), 100)
        h1 = hasher.hasher(os.path.join(BASE, 'different_data'), 100)
        self.assertNotEqual(h0, h1)

    @mock.patch('arthash.hasher.HASH_CLASS', autospec=True)
    def test_calls(self, HASH_CLASS):
        calls = []

        class MockHasher:
            def __init__(self, *args, **kwds):
                self.hasher = hashlib.sha256(*args, **kwds)

            def update(self, b):
                self.hasher.update(b)
                calls.append(b)

            def hexdigest(self):
                return self.hasher.hexdigest()

        HASH_CLASS.side_effect = MockHasher
        h0 = hasher.hasher(os.path.join(BASE, 'data'), 4)
        self.assertEqual(h0, DATA_HASH)
        self.assertEqual(
            calls,
            [b'data',
             b'bar.txt',
             b'Bar ',
             b'bar ',
             b'bar\n',
             b'foo.txt',
             b'Foo ',
             b'foo ',
             b'foo\n',
             b'sub/fred.txt',
             b'Fred',
             b' is ',
             b'red.',
             b'\n',
             b'sub/stuff.json',
             b'{}\n'])
