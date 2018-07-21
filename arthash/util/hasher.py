######
#                   DANGER DANGER DANGER
#
#    CHANGING ANYTHING IN THIS FILE CAN CHANGE THE WHOLE HASH
#    AND POTENTIALLY MAKE ALL HISTORICAL HASHES INVALID!
#

import hashlib, os

HASH_CLASS = hashlib.sha256
EXCLUDED_PREFIXES = '.'
SEPARATOR = b'\0'


def hasher(root, chunksize):
    """
    Return the artHash of all the documents at or below this on in the
    filesystem, listed recursively in sorted order as defined by the
    function walk(), with documents or directories that start with a
    '.' excluded from this list.

    This hasher is fixed and reproducible.  The return value is not dependent
    on the chunksize.
    """
    return _hash_each(_all_items(root, chunksize))


def record_hash(*, art_hash, public_key, record_hash, signature, timestamp):
    """
    Return the record_hash for a record with exactly these five fields.

    This function is fixed and reproducible.
    """
    return _hash_each((art_hash, public_key, record_hash, signature, timestamp))


def walk(root):
    """Yield each document below root, except excluded ones."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = _exclude(dirnames)
        for f in _exclude(filenames):
            path = os.path.join(dirpath, f)
            yield os.path.relpath(path, root)


def _hash_each(items):
    """Create a digest, update with each item and return the hexdigest."""
    digest = HASH_CLASS()

    for i in items:
        b = i.encode() if isinstance(i, str) else i
        digest.update(b)

    return digest.hexdigest()


def _file_chunks(filename, chunksize):
    """Yield a series of chunks from a binary file"""
    with open(filename, 'rb') as fp:
        while True:
            buf = fp.read(chunksize)
            if not buf:
                return
            yield buf


def _all_items(root, chunksize):
    """Yields all the items that get hashed"""
    yield os.path.basename(root)

    if not os.path.isdir(root):
        yield SEPARATOR
        yield from _file_chunks(root, chunksize)

        return

    for filename in sorted(walk(root)):
        full_filename = os.path.join(root, filename)

        yield SEPARATOR
        yield filename

        yield SEPARATOR
        yield from _file_chunks(full_filename, chunksize)


def _exclude(files):
    for f in files:
        if not any(f.startswith(p) for p in EXCLUDED_PREFIXES):
            yield f
