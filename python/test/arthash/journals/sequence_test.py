import json, os, unittest
from unittest.mock import mock_open, patch, DEFAULT
from arthash.journals import sequence


class JournalTest(unittest.TestCase):
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

    @patch.multiple('arthash.journals.sequence', autospec=True,
                    isdir=DEFAULT, listdir=DEFAULT)
    def test_last_file2(self, listdir, isdir):
        directory = {
            'journals': ['00', '01', '02', 'index.html'],
            'journals/02': ['00.json', '01.json', 'index.html'],
        }
        isdir.side_effect = lambda f: not f.endswith('.json')
        listdir.side_effect = directory.__getitem__

        self.assertEqual(sequence.last_file('journals'), 'journals/02/01.json')
