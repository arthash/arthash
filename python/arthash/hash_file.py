import hashlib, json, requests, sys
from . import hasher

CHUNKSIZE = 100000000
SUFFIXES = ['.json', '.txt']
CERT_SUFFIXES = ['.arthash' + s for s in SUFFIXES]

QUERY_PATTERN = '{protocol}://{host}:{port}/{path}?{arthash}'
JOURNAL_PATTERN = '{protocol}://{host}/{path}'

QUERY_HOST = 'http://arthash.org'
PORT = 6666


def make_hash(root):
    return hasher.hasher(root, CHUNKSIZE)


def is_cert(cert):
    return any(cert.endswith(s) for s in CERT_SUFFIXES)


def check_hash(root, cert):
    if not is_cert(cert):
        raise ValueError('Neither file is a cert')

    if is_cert(root):
        raise ValueError('Both files are certs')

    cert_data = json.load(open(cert))

    try:
        arthash_cert = cert_data['arthash']
        journal_page = cert_data['journal_page']
    except KeyError as e:
        raise ValueError('No "%s" in cert %s' % (e.args[0], cert))

    arthash_actual = make_hash(root)
    if arthash_actual != arthash_cert:
        raise ValueError('arthashes do not match')

    return journal_page


def register_hash(root):
    arthash = make_hash(root)
    return arthash


def main(root, cert=None, *rest):
    if rest:
        raise ValueError('Must drop either one or two items')

    if not cert:
        return register_hash(root)

    if not is_cert(cert):
        root, cert = cert, root

    return check_hash(root, cert)


if __name__ == '__main__':
    main(*sys.argv[1:])
