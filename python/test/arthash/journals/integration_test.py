import json, os, random, shutil, sys
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import journals


class IntegrationTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_integration(self):
        self.fs.create_dir('journals')
        hf = journals.Journals('journals')
        return hf


def _random_hash():
    return ''.join(hex(random.randrange(16)) for i in range(64))


def _run_integration_test(directory, count, remove):
    random.seed(0)
    if remove and os.path.exists(directory):
        shutil.rmtree(directory)

    hf = journals.Journals(directory)
    for i in range(count):
        hf.add_hash(_random_hash())


def _main(directory, count=256 * 256 + 1, remove=False or 'true'):
    remove = remove and remove.lower().startswith('t')
    os.makedirs(directory, exist_ok=True)
    _run_integration_test(directory, int(count), remove)


if __name__ == '__main__':
    _main(*sys.argv[1:])
