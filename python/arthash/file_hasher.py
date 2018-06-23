import hashlib, json, requests, sys
from . import hasher

CHUNKSIZE = 100000000
SUFFIXES = ['.json', '.txt']
CERT_SUFFIXES = ['.arthash' + s for s in SUFFIXES]

QUERY_PATTERN = '{protocol}://{host}:{port}{path}?{arthash}'
JOURNAL_PATTERN = '{protocol}://{host}/{path}'

QUERY_DEFAULTS = {
    # 'protocol': 'https',
    # 'host': 'arthash.org',
    'protocol': 'http',
    'host': 'localhost',
    'port': 7887,
    'path': '',
}


def make_hash(document):
    return hasher.hasher(document, CHUNKSIZE)


def is_cert(cert):
    return any(cert.endswith(s) for s in CERT_SUFFIXES)


def check_hash(document, cert):
    if not is_cert(cert):
        raise ValueError('Neither file is a cert')

    if is_cert(document):
        raise ValueError('Both files are certs')

    cert_data = json.load(open(cert))

    try:
        arthash_cert = cert_data['arthash']
        journal_page = cert_data['journal_page']
    except KeyError as e:
        raise ValueError('No "%s" in cert %s' % (e.args[0], cert))

    arthash_actual = make_hash(document)
    if arthash_actual != arthash_cert:
        raise ValueError('arthashes do not match')

    return journal_page


def register_hash(document):
    arthash = make_hash(document)
    return arthash


def main(document, cert=None, *rest):
    if rest:
        raise ValueError('Must drop either one or two items')

    if not cert:
        return register_hash(document)

    if not is_cert(cert):
        document, cert = cert, document

    return check_hash(document, cert)


if __name__ == '__main__':
    main(*sys.argv[1:])
