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
    h = HASH_CLASS()

    def hash_file(filename):
        fh = HASH_CLASS()
        with open(os.path.join(filename), 'rb') as f:
            chunk = f.read(chunksize)
            while chunk:
                fh.update(chunk)
                chunk = f.read(chunksize)
        h.update(fh.hexdigest().encode())

    h.update(os.path.basename(document).encode())

    if os.path.isdir(document):
        for filename in walk(document):
            h.update(filename.encode())
            hash_file(os.path.join(document, filename))
    else:
        hash_file(document)

    return h.hexdigest()


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
