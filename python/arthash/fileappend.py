# A unique appender to a file with a size limit.

import contextlib, datetime, fcntl, os

HASH_LENGTH = 64


@contextlib.contextmanager
def locked_append(filename, open=open, flock=fcntl.flock):
    """Lock filename for append-only."""
    fd = open(filename, 'a')
    flock(fd, fcntl.LOCK_EX)
    try:
        yield fd
    finally:
        flock(fd, fcntl.LOCK_UN)


def check_size(filename, max_file_size, stat=os.stat):
    size = stat(filename).st_size
    if max_file_size < size + HASH_LENGTH:
        raise IOError('Out of space for file %s:  %d, %d, %d' % (
            filename, max_file_size, size))


def check_hash(hash_code):
    if len(hash_code) != HASH_LENGTH:
        # It might be really long, so don't even report it.
        raise ValueError('Wrong hash code length %s' % len(hash_code))

    if not hash_code.islower():
        # For definiteness, only accept lower case hashes.
        raise ValueError('Hashes must be lower case')
    try:
        int(hash_code, 16)
    except:
        raise ValueError('Hashes must be in hex')

   # TODO: check for semantic content (spam, profanity)
   # Out of 0123456789abcdef, with morphisms, that's abcdefoliehsg
   # so forming spam is challenging but not impossible.


def append_hash(filename, hash_code, max_file_size=None):
    """Atomically append to a file using flock.

    Returns the number of bytes written if it was successful, or throws
    an exception if not.  Either writes atomically, or throws an
    exception - retries are possible.  If `max_file_size` is set, the
    file won't be allowed to exceed that size and this routine will
    throw an exception if it does.
    """
    check_hash(hash_code)
    with locked_append(filename) as fd:
        max_file_size and check_size(filename, max_file_size)

        fd.write(datetime.datetime.utcnow().isoformat())
        fd.write(' ')
        fd.write(hash_code)
        fd.write('\n')
