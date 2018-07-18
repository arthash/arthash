import importlib, os, setuptools, subprocess, sys

NAME = 'arthash'
OWNER = 'arthash'

VERSION_FILE = os.path.join(os.path.dirname(__file__), NAME, 'VERSION')
VERSION = open(VERSION_FILE).read().strip()

URL = 'http://github.com/{OWNER}/{NAME}'.format(**locals())
DOWNLOAD_URL = '{URL}/archive/{VERSION}.tar.gz'.format(**locals())

INSTALL_REQUIRES = open('requirements.txt').read().splitlines()
TESTS_REQUIRE = open('test_requirements.txt').read().splitlines()

PACKAGES = setuptools.find_packages(exclude=['test'])

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

SETUPTOOLS_VERSION = '18.5'
SETUPTOOLS_ERROR = """

Your version of setuptools is %s but this needs version %s or greater.

Please type:

    pip install -U setuptools pip

and then try again.
"""


sversion = setuptools.version.__version__
if sversion < SETUPTOOLS_VERSION:
    raise ValueError(SETUPTOOLS_ERROR % (sversion, SETUPTOOLS_VERSION))

setuptools.setup(
    name='arthash',
    version=VERSION,
    description='arthash - hash all the things',
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    license='MIT',
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    tests_require=TESTS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    keywords=['hashing'],
    include_package_data=True,
    scripts=['scripts/artHashEr', 'scripts/artHashD'],
)
