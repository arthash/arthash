import importlib, os, setuptools, subprocess, sys

NAME = 'arthash'
OWNER = 'arthash'
SOURCE = 'python'

VERSION_FILE = os.path.join(os.path.dirname(__file__), SOURCE, NAME, 'VERSION')
VERSION = open(VERSION_FILE).read().strip()

URL = 'http://github.com/{OWNER}/{NAME}'.format(**locals())
DOWNLOAD_URL = '{URL}/archive/{VERSION}.tar.gz'.format(**locals())

INSTALL_REQUIRES = open('requirements.txt').read().splitlines()
TESTS_REQUIRE = open('test_requirements.txt').read().splitlines()


if setuptools.version.__version__ < '18.5':
    # Work around https://github.com/pyca/cryptography/issues/4352
    print('Upgrading setuptools from version', setuptools.version.__version__)
    subprocess.check_call(('pip', 'install', '-U', 'setuptools'))
    importlib.reload(subprocess)
    print('Setuptools is now version', setuptools.version.__version__)

setuptools.setup(
    name='arthash',
    version=VERSION,
    description='arthash - hash all the things',
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    license='MIT',
    packages=setuptools.find_packages(
        include=['python'],
        exclude=['python/test']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=TESTS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    keywords=['hashing'],
    include_package_data=True,
)
