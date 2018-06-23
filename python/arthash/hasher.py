######
#                   DANGER DANGER DANGER
#
#    CHANGING ANYTHING IN THIS FILE CAN CHANGE THE WHOLE HASH
#    AND POTENTIALLY MAKE ALL HISTORICAL HASHES INVALID!
#

import hashlib, os

HASH_CLASS = hashlib.sha256
EXCLUDED_PREFIXES = '.'


def hasher(root, chunksize):
    h = HASH_CLASS()

    for filename in sorted(_walk(root)):
        h.update(filename.encode())

        with open(os.path.join(root, filename), 'rb') as f:
            chunk = f.read(chunksize)
            while chunk:
                h.update(chunk)
                chunk = f.read(chunksize)

    return h.hexdigest()


def _walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = _exclude(dirnames)
        for f in _exclude(filenames):
            path = os.path.join(dirpath, f)
            yield os.path.relpath(path, root)


def _exclude(files):
    for f in files:
        if not any(f.startswith(p) for p in EXCLUDED_PREFIXES):
            yield f
