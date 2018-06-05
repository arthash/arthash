######
######                   DANGER DANGER DANGER
######
######    CHANGING ANYTHING IN THIS FILE CAN CHANGE THE WHOLE HASH
######    AND POTENTIALLY MAKE ALL HISTORICAL HASHES INVALID!
######

import hashlib

HASH_CLASS = hashlib.sha256
EXCLUDED_PREFIXES = '.'


def hasher(root, chunksize):
    h = HASH_CLASS()

    for filename in sorted(walk()):
        h.update(filename.encode())

        with open(filename, 'rb') as f:
            chunk = f.read(chunksize)
            while chunk:
                h.update(chunk)
                chunk = f.read(chunksize)

    return h.hexdigest()


def exclude(files):
    for f in files:
        if not any(f.startswith(p) for p in EXCLUDED_PREFIXES):
            yield f


def walk(root):
    if os.path.isfile(root):
        yield root

    else:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = exclude(dirnames)
            filenames[:] = exclude(filenames)
            yield from (os.path.join(dirpath, f) for f in filenames)
