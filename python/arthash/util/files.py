import os
from . import constants, hasher

SUFFIXES = ['.json', '.txt']
CERT_SUFFIXES = ['.arthash' + s for s in SUFFIXES]


def is_certificate(file):
    return any(file.endswith(s) for s in CERT_SUFFIXES)


def hash_document(document):
    return hasher.hasher(document, constants.CHUNKSIZE)


def is_journal_file(f):
    f = os.path.basename(f)
    if not f.startswith('.'):
        _, suffix = os.path.splitext(f)
        return suffix in ('', '.json')


def last_file(f):
    while os.path.isdir(f):
        dfiles = [f for f in os.listdir(f) if is_journal_file(f)]
        if not dfiles:
            return
        f = os.path.join(f, sorted(dfiles)[-1])
    return f
