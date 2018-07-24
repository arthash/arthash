import hashlib, os, unittest
from arthash.util import hasher
from unittest import mock


class HasherTest(unittest.TestCase):
    maxDiff = 10000

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
        self.assertEqual(h0 != h1, hasher.HASH_ROOT_ITEM)

    def test_different(self):
        h0 = hasher.hasher(BASE_DATA, 100)
        h1 = hasher.hasher(os.path.join(BASE, 'different_data'), 100)
        self.assertNotEqual(h0, h1)

    def test_record_hash(self):
        kwds = {'art_hash': 'a', 'public_key': 'b', 'record_hash': 'c',
                'signature': 'd', 'timestamp': 'e'}
        h = hasher.record_hash(**kwds)
        self.assertEqual(h, RECORD_HASH)

    @mock.patch('arthash.util.hasher.HASH_CLASS', autospec=True)
    def test_calls(self, HASH_CLASS):
        calls = []

        class MockHasher:
            def __init__(self, *args, **kwds):
                self.hasher = hashlib.sha256(*args, **kwds)
                calls.append(b'! create !')

            def update(self, b):
                self.hasher.update(b)
                calls.append(b)

            def digest(self):
                return self.hasher.digest()

            def hexdigest(self):
                return self.hasher.hexdigest()

        HASH_CLASS.side_effect = MockHasher
        h0 = hasher.hasher(BASE_DATA, 4)
        self.assertEqual(h0, DATA_HASH)
        self.assertEqual(calls, HASH_CALLS)


BASE = os.path.dirname(__file__)
BASE_DATA = os.path.join(BASE, 'data')
IDENTICAL_DATA = os.path.join(BASE, 'identical_data', 'data')
DATA_HASH = 'e3a9b8f0b0dcb706c0234111b3b2a4a6793b0db5d039090a74f307d9dad7611d'
RECORD_HASH = '59944b2620627fdafbcfbdb4b8effb6381d568f4136f4e0cd609679a451b6cf0'
HASH_CALLS = [
    b'! create !',
    hasher.Salt.ITEM[0],
    hasher.SEPARATOR,
    b'bar.txt',
    hasher.SEPARATOR,
    b'Bar ',
    b'bar ',
    b'bar\n',
    hasher.SEPARATOR,
    b'foo.txt',
    hasher.SEPARATOR,
    b'Foo ',
    b'foo ',
    b'foo\n',
    hasher.SEPARATOR,
    b'sub/fred.txt',
    hasher.SEPARATOR,
    b'Fred',
    b' is ',
    b'red.',
    b'\n',
    hasher.SEPARATOR,
    b'sub/stuff.json',
    hasher.SEPARATOR,
    b'{}\n',
    b'! create !',
    b',QwpK}_}D(r_p]L/$>f-{8-~I_:DIJH][I_C51u-<}~oJw/qE(W{1*#[;:>GpNg-',
    b'\xf0\xbc\x121=\xa0W\xa8{1.\xff\x17\xef,X\xa7\xcd\xbf\xca\x943s\xe3\n\x968v'
    b'h\xac\x9fu']
