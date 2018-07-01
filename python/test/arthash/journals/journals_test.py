import json, os, unittest
from unittest.mock import mock_open, patch, DEFAULT
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import journals

BASE = os.path.dirname(__file__)

DATA_HASH1 = '9b36b58806fa34131ce330c18a4bb01f73d70413da84c9d3e744e4cf0ea00101'
DATA_HASH2 = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'

TIMESTAMP1 = '2018-06-21T13:11:04.658170'
TIMESTAMP2 = '2018-06-22T13:11:04.658170'

RECORD1 = [[DATA_HASH1, TIMESTAMP1]]
RECORD2 = [[DATA_HASH2, TIMESTAMP2]]


class JournalsTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @patch('arthash.journals.journals.timestamp', autospec=True)
    def test_journals(self, timestamp):
        timestamp.return_value = TIMESTAMP2

        contents = json.dumps(RECORD1)
        self.fs.create_file('journals/index.html')
        self.fs.create_file('journals/00/index.html')
        self.fs.create_file('journals/01/index.html')
        self.fs.create_file('journals/02/index.html')
        self.fs.create_file('journals/02/00.json')
        self.fs.create_file('journals/02/01.json', contents=contents)

        hf = journals.Journals('journals')
        self.assertEqual(hf.last, 'journals/02/01.json')
        self.assertEqual(hf.page, RECORD1)

        hf.add_hash(DATA_HASH2)

        self.assertEqual(hf.page, RECORD1 + RECORD2)
        actual_page = json.load(open('journals/02/01.json'))
        self.assertEqual(actual_page, hf.page)

    @patch('arthash.journals.journals.timestamp', autospec=True)
    def test_overflow1(self, timestamp):
        timestamp.return_value = TIMESTAMP2

        contents = json.dumps(RECORD1 * 256)
        self.fs.create_file('journals/index.html')
        self.fs.create_file('journals/00/index.html')
        self.fs.create_file('journals/01/index.html')
        self.fs.create_file('journals/02/index.html')
        self.fs.create_file('journals/02/00/index.html')
        self.fs.create_file('journals/02/00/00/index.html')
        self.fs.create_file('journals/02/00/01/index.html')
        self.fs.create_file('journals/02/00/01/00.json', contents=contents)

        hf = journals.Journals('journals')
        self.assertEqual(hf.last, 'journals/02/00/01/00.json')
        self.assertEqual(hf.page, RECORD1 * 256)

        hf.add_hash(DATA_HASH2)

        self.assertEqual(hf.last, 'journals/02/00/01/01.json')
        self.assertEqual(hf.page, [[DATA_HASH2, TIMESTAMP2]])

        actual_page = json.load(open('journals/02/00/01/01.json'))
        self.assertEqual(actual_page, hf.page)

    @patch('arthash.journals.journals.timestamp', autospec=True)
    def test_overflow2(self, timestamp):
        timestamp.return_value = TIMESTAMP2
        self.fs.create_dir('journals')

        hf = journals.Journals('journals')
        self.assertEqual(hf.last, 'journals/00/00/00/00.json')
        self.assertEqual(hf.page, [])

        hf.add_hash(DATA_HASH2)

        self.assertEqual(hf.last, 'journals/00/00/00/00.json')
        self.assertEqual(hf.page, [[DATA_HASH2, TIMESTAMP2]])

        actual_page = json.load(open('journals/00/00/00/00.json'))
        self.assertEqual(actual_page, hf.page)
