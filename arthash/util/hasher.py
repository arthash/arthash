######
#                   DANGER DANGER DANGER
#
#    CHANGING ANYTHING AT ALL IN THIS FILE CAN POTENTIALLY CHANGE THE WHOLE
#    HASH AND MAKE ALL HISTORICAL HASHES INVALID!
#

import binascii, hashlib, os

HASH_CLASS = hashlib.sha256
EXCLUDED_PREFIXES = '.'


def hasher(root, chunksize):
    """
    Return the artHash of all the documents at or below this on in the
    filesystem, listed recursively in sorted order as defined by the
    function walk(), with documents or directories that start with a
    '.' excluded from this list.

    This hasher is fixed and reproducible.  The return value is not dependent
    on the chunksize.
    """
    items = _items(root, chunksize)
    return _hasher(items, Salt.ITEM)


def record_hash(*, art_hash, public_key, record_hash, signature, timestamp):
    """
    Return the record_hash for a record with exactly these five fields.

    This function is fixed and reproducible.
    """
    items = (art_hash, public_key, record_hash, signature, timestamp)
    return _hasher(items, Salt.RECORD)


def walk(root):
    """Yield each document below root, except excluded ones."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = _exclude(dirnames)
        for f in _exclude(filenames):
            path = os.path.join(dirpath, f)
            yield os.path.relpath(path, root)


def to_hex(s):
    # For Python 3.4 compatibility
    return binascii.hexlify(s).decode()


def _hasher(items, salts):
    """Hash an iterable of items once for each salt and return a hexdigest"""
    for salt in salts:
        items = [_hash_once(items, salt)]

    return to_hex(items[0])


def _hash_once(items, salt):
    """Hash one time with a given salt"""
    digest = HASH_CLASS()
    digest.update(salt)

    for i in items:
        b = i.encode() if isinstance(i, str) else i
        digest.update(b)

    return digest.digest()


def _items(root, chunksize):
    """Yields all the items that get hashed"""
    if not os.path.isdir(root):
        yield Salt.FILE[0]
        yield from _file_chunks(root, chunksize)

        return

    for filename in sorted(walk(root)):
        yield Salt.FILE[1]

        full_filename = os.path.join(root, filename)
        yield filename

        yield Salt.FILE[2]
        yield from _file_chunks(full_filename, chunksize)


def _file_chunks(filename, chunksize):
    """Yield a series of chunks from a binary file"""
    with open(filename, 'rb') as fp:
        while True:
            buf = fp.read(chunksize)
            if not buf:
                return
            yield buf


def _exclude(files):
    for f in files:
        if not any(f.startswith(p) for p in EXCLUDED_PREFIXES):
            yield f


class Salt:
    ITEM = (
        b'b%IZfHOB5^T"d;(H"ok76J!/H3}W0/lJE{K1N`wa}tZ=E)IQ<>|1GCT<xY?=oP1$',
        b',QwpK}_}D(r_p]L/$>f-{8-~I_:DIJH][I_C51u-<}~oJw/qE(W{1*#[;:>GpNg-')

    RECORD = (
        b'{AGbv]u)<xay>*W-rkS-ZacZwh@~xJ>ztvZiXr^lSb+zhc=!G$.JnWqXLPyUBwT=',
        b'rxz{dk0@hSu?.iweXzyv3OE`S[0(Kn!9[1D/tv{pAZ99=ZV*dP^>w&@bju.1*kPK')

    FILE = [
        b'.8=E:puyS(@u$jqb-T#E+EsY?Da7hJ,u,JA(qNTOtQeihr^<|2KVg*i;#^e*PZ,d',
        b'|+D,sPt$wt[]w^7Cv/QNS?Fm|R)K]-m!"g1/Z/+Iu_~:{{/?iivr{UPKZ3".qz-w',
        b'2}X4J#.vZ&AV"89EMXUHH}aDXX;`(9$L;5MI*;r{XB0"rTlP"r{U+,=5$A+{iX/M']
