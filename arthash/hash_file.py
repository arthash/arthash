import hashlib, sys
from . import files

"""
Originally from arthash.app/Contents/document.wflow
"""

######    BEGIN DANGER
######    CHANGING ANYTHING BETWEEN THESE LINES WILL CHANGE THE WHOLE
######    HASH AND POTENTIALLY MAKE ALL HISTORICAL HASHES INVALID!

def directory_hasher(root):
    h = HASHER()

    for f in files.all_files_under(root, EXCLUDE_PREFIXES):
        h.update(f.encode())

        for chunk in files.chunk_reader(f, CHUNKSIZE):
            h.update(chunk)

    return h.hexdigest()


######    END DANGER

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


def main(root, cert=None):
    if not cert:
       return make_hash(root)

    if is_cert(cert):
        return verify_hash(root, cert)

    return verify_hash(cert, root)


if __name__ == '__main__':
    main(*sys.argv[1:])


def OLD_add_hash_to(fname, **kwds):
    fhash = directory_hash(fname, **kwds)
    open(fname + '.sha256.txt', 'w').write(fhash + '\n')


def OLD_main():
    for filename in sys.argv[1:]:
        try:
            add_hash_to(filename)
        except Exception as e:
            print('Exception |', e, '| trying to hash', filename)
