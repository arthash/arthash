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
        yield os.path.basename(document).encode()

        if os.path.isdir(document):
            for filename in walk(document):
                yield filename.encode()
                yield from file_blocks(os.path.join(document, filename))
        else:
            yield from file_blocks(document)

    digest = HASH_CLASS()
    for b in all_blocks():
        digest.update(b)

    return digest.hexdigest()


def walk(document):
    results = []
    for dirpath, dirnames, filenames in os.walk(document):
        dirnames[:] = exclude(dirnames)
        for f in exclude(filenames):
            path = os.path.join(dirpath, f)
            results.append(os.path.relpath(path, document))

    return results.sort() or results


def exclude(files):
    for f in files:
        if not any(f.startswith(p) for p in EXCLUDED_PREFIXES):
            yield f
