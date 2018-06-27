import hashlib, os, unittest
from arthash import hasher
from unittest import mock

BASE = os.path.dirname(__file__)
BASE_DATA = os.path.join(BASE, 'data')
IDENTICAL_DATA = os.path.join(BASE, 'identical_data', 'data')
DATA_HASH = 'f23fd0692a4645bac4ca46eabea0e336f8b5a3677a154ad2dcf78c9ec24d95e5'


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

    @mock.patch('arthash.hasher.HASH_CLASS', autospec=True)
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
             '! create !',
             b'Bar ',
             b'bar ',
             b'bar\n',
             b'9991fc202dd65996570a011278b77105abcc2cb3c5955ac9ffc1f4a0c1839568',
             b'foo.txt',
             '! create !',
             b'Foo ',
             b'foo ',
             b'foo\n',
             b'4022b6217dfa5312830e5b005726a362ee438a237f42d5d257ab48cb96b8ae8f',
             b'sub/fred.txt',
             '! create !',
             b'Fred',
             b' is ',
             b'red.',
             b'\n',
             b'83553dcb8323a817ebd706c3bd440f56b0f1cd7844e6159af8bedbede5924703',
             b'sub/stuff.json',
             '! create !',
             b'{}\n',
             b'ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356'
             ])
