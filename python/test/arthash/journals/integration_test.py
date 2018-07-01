import json, os, random
from unittest.mock import patch
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import journals


def _random_hash():
    return ''.join(hex(random.randint(16)) for i in range(64))


class IntegrationTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_integration(self):
        self.fs.create_dir('journals')
        hf = journals.Journals('journals')
        return hf
