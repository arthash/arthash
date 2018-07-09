import datetime, json, os, random, shutil, sys, tempfile, unittest, zipfile
from unittest.mock import patch
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import keeper, organization
from arthash.util import hasher


class IntegrationTest(unittest.TestCase):
    def do_test(self, i):
        errors = list(Reader(i).test())
        self.assertEqual(errors, [])

    def test_0(self):
        self.do_test(0)

    def test_1(self):
        self.do_test(1)

    def test_2(self):
        self.do_test(2)

    def test_3(self):
        self.do_test(3)


class IntegrationDesc:
    TESTS = (
        (18, 2, 2),
        (360, 4, 3),
        (180, 2, 4),
        (1100, 256, 4),
    )

    BASE_DIR = os.path.dirname(__file__)
    JOURNAL_DIR = os.path.join(BASE_DIR, 'journals', 'journal')
    ZIP_FORMAT = JOURNAL_DIR + '-{count}-{org.page_size}-{org.levels}.zip'
    TIME_DELTA = datetime.timedelta(seconds=2)
    TIMESTAMP = datetime.datetime(2018, 7, 6)
    HEX = '0123456789abcdef'

    def __init__(self, count, page_size, levels):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.directory = self.temp_dir.name
        self.count = count
        self.org = organization.Organization(page_size, levels)
        self.time = self.TIMESTAMP

    @property
    def zipname(self):
        return self.ZIP_FORMAT.format(**vars(self))

    def add_hashes(self):
        hf = keeper.Keeper(self.directory, self.org)
        random.seed(0)

        with patch('arthash.journals.keeper.timestamp') as timestamp:
            timestamp.side_effect = self.timestamp

            for i in range(int(self.count)):
                hf.add_record(self.random_hash())

    def random_hash(self):
        return ''.join(self.HEX[random.randrange(16)] for i in range(64))

    def timestamp(self):
        self.time += self.TIME_DELTA
        return self.time.isoformat()


class Writer(IntegrationDesc):
    def write(self):
        self.add_hashes()
        zpf = zipfile.ZipFile(self.zipname, 'w', zipfile.ZIP_DEFLATED)

        for rel_path in hasher.walk(self.directory):
            abs_path = os.path.join(self.directory, rel_path)
            zpf.write(abs_path, rel_path)
        print('Wrote', self.count, 'hashes to', self.zipname)

    @classmethod
    def write_all(cls):
        for test in cls.TESTS:
            cls(*test).write()


class Reader(IntegrationDesc):
    def __init__(self, i):
        super().__init__(*self.TESTS[i])

    def test(self):
        # Yield a series of error messages.
        self.add_hashes()

        zpf = zipfile.ZipFile(self.zipname)
        actual_names = set(hasher.walk(self.directory))
        zip_names = set(zpf.namelist())
        az, za = actual_names - zip_names, zip_names - actual_names

        for name in actual_names - zip_names:
            yield 'Name %s was unknown' % name

        for name in zip_names - actual_names:
            yield 'Name %s was missing' % name

        for name in sorted(set(actual_names) & set(zip_names)):
            expected = zpf.open(name).read().decode()
            actual_name = os.path.join(self.directory, name)
            actual = open(actual_name).read()
            if actual != expected:
                error = BAD_CONTENTS_ERROR.format(**locals())
                print(error)
                yield error

    def write(self):
        self.add_hashes()
        zpf = zipfile.ZipFile(self.zipname, 'w', zipfile.ZIP_DEFLATED)

        for rel_path in hasher.walk(self.directory):
            abs_path = os.path.join(self.directory, rel_path)
            zpf.write(abs_path, rel_path)
        print('Wrote', self.count, 'hashes to', self.zipname)

    @classmethod
    def write_all(cls):
        for test in cls.TESTS:
            cls(*test).write()


BAD_CONTENTS_ERROR = """\
Contents differed for {name}:
    Actual:
----
{actual}

----
    Expected:
----
{expected}

"""

if __name__ == '__main__':
    Writer.write_all()
