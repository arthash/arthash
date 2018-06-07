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

    cert_data = json.load(open(filename))
    arthash = hasher.hasher(root)



def main(root, cert=None):
    if not cert:
       make_hash(root)

    elif is_cert(cert):
       verify_hash(root, cert)

    else:
        verify_hash(cert, root)


if __name__ == '__main__':
    main(*sys.argv[1:])


def OLD_add_hash_to(root):
    fhash = hasher.hasher(root)

    open(fname + '.sha256.txt', 'w').write(fhash + '\n')


def OLD_main():
    for filename in sys.argv[1:]:
        try:
            add_hash_to(filename)
        except Exception as e:
            print('Exception |', e, '| trying to hash', filename)
