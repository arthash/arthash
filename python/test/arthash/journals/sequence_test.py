import json, os, unittest
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import sequence


class JournalTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_next_file(self):
        self.assertEqual(sequence.next_file('00/00/00/00.json'),
                         '00/00/00/01.json')
        self.assertEqual(sequence.next_file('00/00/00/01.json'),
                         '00/00/00/02.json')
        self.assertEqual(sequence.next_file('00/00/00/fe.json'),
                         '00/00/00/ff.json')
        self.assertEqual(sequence.next_file('00/00/00/ff.json'),
                         '00/00/01/00.json')
        self.assertEqual(sequence.next_file('00/00/01/00.json'),
                         '00/00/01/01.json')
        self.assertEqual(sequence.next_file('00/00/ff/ff.json'),
                         '00/01/00/00.json')
        self.assertEqual(sequence.next_file('00/ff/ff/ff.json'),
                         '01/00/00/00.json')
        self.assertEqual(sequence.next_file('ff/ff/ff/ff.json'),
                         '100/00/00/00.json')

    def test_last_file2(self):
        self.fs.create_file('journals/index.html')
        self.fs.create_file('journals/00/index.html')
        self.fs.create_file('journals/01/index.html')
        self.fs.create_file('journals/02/index.html')
        self.fs.create_file('journals/02/00.json')
        self.fs.create_file('journals/02/01.json')

        self.assertEqual(sequence.last_file('journals'), 'journals/02/01.json')
