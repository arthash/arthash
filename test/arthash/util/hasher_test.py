import hashlib, os, unittest
from arthash.util import hasher
from unittest import mock

BASE = os.path.dirname(__file__)
BASE_DATA = os.path.join(BASE, 'data')
IDENTICAL_DATA = os.path.join(BASE, 'identical_data', 'data')
DATA_HASH = 'a7628a45fa12cfa8859e8bd7ceb8b2b399e85557e2c6b9b2a93351044285dc20'


class HasherTest(unittest.TestCase):
    def test_simple(self):
        h1 = hasher.hasher(BASE_DATA, 10)
        self.assertEqual(h1, DATA_HASH)

    def test_chunksize(self):
        h0 = hasher.hasher(BASE_DATA, 4)
        h1 = hasher.hasher(BASE_DATA, 10)
        self.assertEqual(h0, h1)

    def test_identical(self):
        h0 = hasher.hasher(BASE_DATA, 4)
        h1 = hasher.hasher(IDENTICAL_DATA, 4)
        self.assertEqual(h0, h1)
        self.assertEqual(h1, DATA_HASH)

    def test_identical_file(self):
        h0 = hasher.hasher(os.path.join(BASE_DATA, 'bar.txt'), 4)
        h1 = hasher.hasher(os.path.join(IDENTICAL_DATA, 'bar.txt'), 4)
        self.assertEqual(h0, h1)

    def test_identical_file_different_name(self):
        h0 = hasher.hasher(os.path.join(BASE_DATA, 'bar.txt'), 4)
        h1 = hasher.hasher(os.path.join(BASE, 'bad.txt'), 4)
        self.assertNotEqual(h0, h1)

    def test_different(self):
        h0 = hasher.hasher(BASE_DATA, 100)
        h1 = hasher.hasher(os.path.join(BASE, 'different_data'), 100)
        self.assertNotEqual(h0, h1)

    @mock.patch('arthash.util.hasher.HASH_CLASS', autospec=True)
    def test_calls(self, HASH_CLASS):
        calls = []

        class MockHasher:
            def __init__(self, *args, **kwds):
                self.hasher = hashlib.sha256(*args, **kwds)
                calls.append('! create !')

            def update(self, b):
                self.hasher.update(b)
                calls.append(b)

            def hexdigest(self):
                return self.hasher.hexdigest()

        HASH_CLASS.side_effect = MockHasher
        h0 = hasher.hasher(BASE_DATA, 4)
        self.assertEqual(h0, DATA_HASH)
        self.assertEqual(
            calls,
            ['! create !',
             b'data',
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
             b'{}\n',
             ])
