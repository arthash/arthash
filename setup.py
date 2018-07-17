from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os, sys

NAME = 'arthash'
OWNER = 'arthash'
SOURCE = 'python'

VERSION_FILE = os.path.join(os.path.dirname(__file__), SOURCE, NAME, 'VERSION')
VERSION = open(VERSION_FILE).read().strip()

URL = 'http://github.com/{OWNER}/{NAME}'.format(**locals())
DOWNLOAD_URL = '{URL}/archive/{VERSION}.tar.gz'.format(**locals())

INSTALL_REQUIRES = open('requirements.txt').read().splitlines()
TESTS_REQUIRE = open('test_requirements.txt').read().splitlines()


# From here: http://pytest.org/2.2.4/goodpractises.html
class RunTests(TestCommand):
    DIRECTORY = 'test'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.DIRECTORY]
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        if errno:
            raise SystemExit(errno)


setup(
    name='arthash',
    version=VERSION,
    description='arthash - hash all the things',
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    license='MIT',
    packages=find_packages(include=['python'], exclude=['python/test']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=TESTS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    cmdclass={'test': RunTests},
    keywords=['hashing'],
    include_package_data=True,
)
