from . import constants, hasher

SUFFIXES = ['.json', '.txt']
CERT_SUFFIXES = ['.arthash' + s for s in SUFFIXES]


def is_certificate(file):
    return any(file.endswith(s) for s in CERT_SUFFIXES)


def hash_document(document):
    return hasher.hasher(document, constants.CHUNKSIZE)
