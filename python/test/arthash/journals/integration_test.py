import json, os, random, shutil, sys
from pyfakefs.fake_filesystem_unittest import TestCase
from arthash.journals import keeper, organization


class IntegrationTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_integration(self):
        hf = keeper.Keeper('journals')
        return hf


def _random_hash():
    return ''.join(hex(random.randrange(16)) for i in range(64))


def run_integration_test(
        directory, count=256 * 256 + 1, remove=False, page_size=256, levels=4):
    random.seed(0)

    if os.path.exists(directory):
        if remove is True or remove and remove.lower().startswith('t'):
            shutil.rmtree(directory)

    org = organization.Organization(int(page_size), int(levels))

    hf = keeper.Keeper(directory, org)
    for i in range(int(count)):
        hf.add_hash(_random_hash())


if __name__ == '__main__':
    run_integration_test(*sys.argv[1:])
