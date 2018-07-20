######
#                   DANGER DANGER DANGER
#
#    CHANGING ANYTHING IN THIS FILE CAN CHANGE THE WHOLE HASH
#    AND POTENTIALLY MAKE ALL HISTORICAL HASHES INVALID!
#

import hashlib, os

HASH_CLASS = hashlib.sha256
EXCLUDED_PREFIXES = '.'


def hasher(document, chunksize):
    def file_blocks(filename):
        with open(filename, 'rb') as fp:
            while True:
                buf = fp.read(chunksize)
                if not buf:
                    return
                yield buf

    def all_blocks():
        yield os.path.basename(document)

        if not os.path.isdir(document):
            yield from file_blocks(document)
            return

        for filename in walk(document):
            yield filename
            yield from file_blocks(os.path.join(document, filename))

    return hash_iterator(all_blocks())


def walk(document):
    results = []
    for dirpath, dirnames, filenames in os.walk(document):
        dirnames[:] = exclude(dirnames)
        for f in exclude(filenames):
            path = os.path.join(dirpath, f)
            results.append(os.path.relpath(path, document))

    results.sort()
    return results


def hash_iterator(it):
    digest = HASH_CLASS()
    for s in it:
        digest.update(s.encode() if isinstance(s, str) else s)

    return digest.hexdigest()


def record_hash(*, art_hash, public_key, signature, timestamp):
    record = art_hash, public_key, signature, timestamp
    return hash_iterator(record)


def exclude(files):
    for f in files:
        if not any(f.startswith(p) for p in EXCLUDED_PREFIXES):
            yield f
