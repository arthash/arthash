import unittest
from arthash.util import files
from pyfakefs.fake_filesystem_unittest import TestCase


class FilesTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_last_file2(self):
        self.fs.create_file('journals/index.html')
        self.fs.create_file('journals/00/index.html')
        self.fs.create_file('journals/01/index.html')
        self.fs.create_file('journals/02/index.html')
        self.fs.create_file('journals/02/00.json')
        self.fs.create_file('journals/02/01.json')

        self.assertEqual(files.last_file('journals'), 'journals/02/01.json')
