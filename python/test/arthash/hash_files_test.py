import json, os, unittest
from unittest.mock import mock_open, patch, DEFAULT
from arthash.hash_files import next_hash_file, last_hash_file, HashFiles

BASE = os.path.dirname(__file__)

DATA_HASH1 = '9b36b58806fa34131ce330c18a4bb01f73d70413da84c9d3e744e4cf0ea00101'
DATA_HASH2 = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'

TIMESTAMP1 = '2018-06-21T13:11:04.658170'
TIMESTAMP2 = '2018-06-22T13:11:04.658170'

RECORD1 = [[DATA_HASH1, TIMESTAMP1]]
RECORD2 = [[DATA_HASH2, TIMESTAMP2]]


class HashFilesTest(unittest.TestCase):
    def test_next_hash_file(self):
        self.assertEqual(next_hash_file('00/00/00/00.json'),
                         '00/00/00/01.json')
        self.assertEqual(next_hash_file('00/00/00/01.json'),
                         '00/00/00/02.json')
        self.assertEqual(next_hash_file('00/00/00/fe.json'),
                         '00/00/00/ff.json')
        self.assertEqual(next_hash_file('00/00/00/ff.json'),
                         '00/00/01/00.json')
        self.assertEqual(next_hash_file('00/00/01/00.json'),
                         '00/00/01/01.json')
        self.assertEqual(next_hash_file('00/00/ff/ff.json'),
                         '00/01/00/00.json')
        self.assertEqual(next_hash_file('00/ff/ff/ff.json'),
                         '01/00/00/00.json')
        self.assertEqual(next_hash_file('ff/ff/ff/ff.json'),
                         '100/00/00/00.json')

    @patch.multiple('arthash.hash_files', autospec=True,
                    isdir=DEFAULT, listdir=DEFAULT)
    def test_last_hash_file2(self, listdir, isdir):
        directory = {
            'root': ['00', '01', '02'],
            'root/02': ['00.json', '01.json'],
        }
        isdir.side_effect = lambda f: not f.endswith('.json')
        listdir.side_effect = directory.__getitem__

        self.assertEqual(last_hash_file('root'), 'root/02/01.json')

    @patch.multiple('arthash.hash_files', autospec=True,
                    isdir=DEFAULT, listdir=DEFAULT, makedirs=DEFAULT,
                    open=DEFAULT, timestamp=DEFAULT)
    def test_hashfiles(self, timestamp, open, makedirs, listdir, isdir):
        directory = {
            'root': ['00', '01', '02'],
            'root/02': ['00.json', '01.json'],
        }

        isdir.side_effect = lambda f: not f.endswith('.json')
        listdir.side_effect = directory.__getitem__
        open.side_effect = mock_open(read_data=json.dumps(RECORD1))
        timestamp.side_effect = lambda: TIMESTAMP2

        hf = HashFiles('root')
        self.assertEqual(hf.last, 'root/02/01.json')
        self.assertEqual(hf.page, RECORD1)

        hf.add_hash(DATA_HASH2)
        self.assertEqual(hf.page, RECORD1 + RECORD2)
        self.assertEqual(get_writes(open), hf.page)

    @patch.multiple('arthash.hash_files', autospec=True,
                    isdir=DEFAULT, listdir=DEFAULT, makedirs=DEFAULT,
                    open=DEFAULT, timestamp=DEFAULT)
    def test_overflow(self, timestamp, open, makedirs, listdir, isdir):
        directory = {
            'root': ['00', '01', '02'],
            'root/02': ['00'],
            'root/02/00': ['00', '01'],
            'root/02/00/01': ['00.json'],
        }

        isdir.side_effect = lambda f: not f.endswith('.json')
        listdir.side_effect = directory.__getitem__
        open.side_effect = mock_open(read_data=json.dumps(RECORD1 * 256))
        timestamp.side_effect = lambda: TIMESTAMP2

        hf = HashFiles('root')
        self.assertEqual(hf.last, 'root/02/00/01/00.json')
        self.assertEqual(hf.page, RECORD1 * 256)

        hf.add_hash(DATA_HASH2)
        self.assertEqual(hf.last, 'root/02/00/01/01.json')
        self.assertEqual(hf.page, [[DATA_HASH2, TIMESTAMP2]])
        self.assertEqual(get_writes(open), hf.page)
        makedirs.assert_called_with('root/02/00/01', exist_ok=True)

    @patch.multiple('arthash.hash_files', autospec=True,
                    isdir=DEFAULT, listdir=DEFAULT, makedirs=DEFAULT,
                    open=DEFAULT, timestamp=DEFAULT)
    def test_overflow2(self, timestamp, open, makedirs, listdir, isdir):
        directory = {'root': []}

        isdir.side_effect = lambda f: not f.endswith('.json')
        listdir.side_effect = directory.__getitem__
        open.side_effect = mock_open()
        timestamp.side_effect = lambda: TIMESTAMP2

        hf = HashFiles('root')
        self.assertEqual(hf.last, 'root/00/00/00/00.json')
        self.assertEqual(hf.page, [])
        makedirs.assert_called_with('root/00/00/00', exist_ok=True)

        hf.add_hash(DATA_HASH2)
        self.assertEqual(hf.last, 'root/00/00/00/00.json')
        self.assertEqual(hf.page, [[DATA_HASH2, TIMESTAMP2]])
        self.assertEqual(get_writes(open), hf.page)


def get_writes(open):
    results = []
    for name, args, kwds in open.side_effect.mock_calls:
        if name.endswith('.write'):
            data, = args
            results.append(data)

    return json.loads(''.join(results))
