import hashlib, json, sys
from . import hasher


CHUNKSIZE = 100000000
SUFFIXES = ['.json', '.txt']
CERT_SUFFIXES = ['.arthash' + s for s in SUFFIXES]


def make_hash(root):
    pass


def is_cert(cert):
    return any(cert.endswith(s) for s in CERT_SUFFIXES)


def verify_hash(root, cert):
    if not is_cert(cert):
        raise ValueError('Neither file is a cert')

    if is_cert(root):
        raise ValueError('Both files are certs')

    cert_data = json.load(open(cert))
    arthash = hasher.hasher(root, CHUNKSIZE)
    return cert_data, arthash


def main(root, cert=None, *rest):
    if rest:
        raise ValueError('Must drop either one or two items')

    if not cert:
        return make_hash(root)

    if not is_cert(cert):
        root, cert = cert, root

    return verify_hash(root, cert)


if __name__ == '__main__':
    main(*sys.argv[1:])
