import unittest
from unittest.mock import patch, DEFAULT
from arthash.journals import journal_files
from . journals_test import get_writes

ONE_INDEX = '        <td><a href="00/index.html"><pre>00</pre></a></td>'
JSON_ONE = '        <td><a href="00.json"><pre>00</pre></a></td>'
JSON_TWO = '        <td><a href="01.json"><pre>01</pre></a></td>'


def table(items):
    return ['<table>'] + list(items) + ['</table>']


def row(items):
    return ['    <tr>'] + list(items) + ['    </tr>']


class LinkLinesTest(unittest.TestCase):
    @patch('arthash.journals.journal_files.listdir', autospec=True,
           listdir=DEFAULT)
    def test_branch_single(self, listdir):
        listdir.return_value = ['00']
        actual = list(journal_files.link_lines('ignore'))
        expected = table(row([ONE_INDEX]))
        self.assertEqual(actual, expected)

    @patch('arthash.journals.journal_files.listdir', autospec=True,
           listdir=DEFAULT)
    def test_branch_many(self, listdir):
        listdir.return_value = ['00'] * 17
        actual = list(journal_files.link_lines('ignore'))
        expected = table(row([ONE_INDEX] * 16) + row([ONE_INDEX]))
        self.assertEqual(actual, expected)

    @patch('arthash.journals.journal_files.listdir', autospec=True,
           listdir=DEFAULT)
    def test_json_double(self, listdir):
        listdir.return_value = ['00.json', '01.json']
        actual = list(journal_files.link_lines('ignore'))
        expected = table(row([JSON_ONE, JSON_TWO]))
        self.assertEqual(actual, expected)


class WriteIndexTest(unittest.TestCase):
    @patch.multiple('arthash.journals.journal_files', autospec=True,
                    listdir=DEFAULT, open=DEFAULT)
    def test_write(self, listdir, open):
        pass
