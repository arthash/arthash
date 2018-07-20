import json, os, unittest
from unittest.mock import patch
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.arthashd import request_handler

BASE = os.path.dirname(__file__)


class RecordKeeperTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def run_test(self, last1, page1, last2, page2):
        if page1:
            self.fs.create_file(last1, contents=json.dumps(page1))
        hf = request_handler.RecordKeeper('journals')

        self.assertEqual(hf.last, last1)
        self.assertEqual(hf.page, page1)
        if page1:
            self.assertEqual(hf.page, json.load(open(hf.last)))

        hf.new_record(
            art_hash=HASH2,
            record_hash=HASH1,
            signature='signature2',
            timestamp=TIMESTAMP2)

        self.assertEqual(hf.last, last2)
        self.maxDiff = 100000
        self.assertEqual(hf.page, page2)
        self.assertEqual(hf.page, json.load(open(hf.last)))

    def test_journals(self):
        self.fs.create_file('journals/index.html')
        self.fs.create_file('journals/00/index.html')
        self.fs.create_file('journals/01/index.html')
        self.fs.create_file('journals/02/index.html')
        self.fs.create_file('journals/02/00.json')

        self.run_test(
            'journals/02/01.json', [RECORD1],
            'journals/02/01.json', [RECORD1, RECORD2])

    def test_overflow1(self):
        self.fs.create_file('journals/index.html')
        self.fs.create_file('journals/00/index.html')
        self.fs.create_file('journals/01/index.html')
        self.fs.create_file('journals/02/index.html')
        self.fs.create_file('journals/02/00/index.html')
        self.fs.create_file('journals/02/00/00/index.html')
        self.fs.create_file('journals/02/00/01/index.html')

        self.run_test(
            'journals/02/00/01/00.json', [RECORD1] * 256,
            'journals/02/00/01/01.json', [RECORD2])

    def test_initial(self):
        self.fs.create_dir('journals')

        self.run_test(
            'journals/00/00/00/00.json', [],
            'journals/00/00/00/00.json', [RECORD2])


HASH1 = '9b36b58806fa34131ce330c18a4bb01f73d70413da84c9d3e744e4cf0ea00101'
HASH2 = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'


TIMESTAMP1 = '2018-06-21T13:11:04.658170'
TIMESTAMP2 = '2018-06-22T13:11:04.658170'

RECORD1 = {
    'art_hash': HASH1,
    'record_hash': HASH2,
    'signature': 'signature1',
    'timestamp': TIMESTAMP1,
}

RECORD2 = {
    'art_hash': HASH2,
    'record_hash': HASH1,
    'signature': 'signature2',
    'timestamp': TIMESTAMP2,
}
