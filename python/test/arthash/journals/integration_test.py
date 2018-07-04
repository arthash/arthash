import datetime, json, os, random, shutil, sys, zipfile
from unittest.mock import patch
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import keeper, organization

HEX = '0123456789abcdef'
BASE_DIR = os.path.dirname(__file__)
JOURNAL_DIR = os.path.join(BASE_DIR, 'journals', 'journal')
TESTS = (
    (18, 2, 2),
    (360, 4, 3),
    (180, 2, 4),
    (1100, 256, 4),
)
TIMESTAMP = datetime.datetime(2018, 7, 6)


class IntegrationTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_integration(self):
        hf = keeper.Keeper('journals')
        return hf


def _random_hash():
    return ''.join(HEX[random.randrange(16)] for i in range(64))


def run_integration_test(
        directory, count=256 * 256 + 1, page_size=256, levels=4):
    org = organization.Organization(int(page_size), int(levels))

    if os.path.exists(directory):
        shutil.rmtree(directory)

    hf = keeper.Keeper(directory, org)

    random.seed(0)

    with patch('arthash.journals.keeper.timestamp') as timestamp:
        timestamp.side_effect = mock_timestamp()

        for i in range(int(count)):
            hf.add_hash(_random_hash())

    return count, org, directory


def make_zip_file(count, org, directory):
    zipname = '%s-%d-%d-%d.zip' % (directory, count, org.page_size, org.levels)
    zipf = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.startswith('.'):
                fname = os.path.join(root, file)
                zipf.write(fname, os.path.relpath(fname, directory))

    return zipname


def write_zipfile(directory, *args):
    count, org, directory = run_integration_test(directory, *args)
    zipname = make_zip_file(count, org, directory)
    shutil.rmtree(directory)

    print('\nCreated', zipname, '\n')


def write_all(directory=JOURNAL_DIR):
    for test in TESTS:
        write_zipfile(directory, *test)


def mock_timestamp():
    time = TIMESTAMP
    delta = datetime.timedelta(seconds=2)

    def timestamp():
        nonlocal time
        time += delta
        return time.isoformat()

    return timestamp


if __name__ == '__main__':
    write_all(*sys.argv[1:])
