import datetime, json, os

from os import listdir, makedirs
from os.path import isdir

open = __builtins__['open']


def last_file(f):
    while isdir(f):
        files = [f for f in listdir(f) if not f.startswith('.')]
        if not files:
            return
        f = os.path.join(f, sorted(files)[-1])
    return f


def next_file(f):
    f, d4_json = os.path.split(f)
    f, d3 = os.path.split(f)
    f, d2 = os.path.split(f)
    f, d1 = os.path.split(f)
    if f:
        raise ValueError(f)

    d4, suffix = os.path.splitext(d4_json)
    if suffix != '.json':
        raise ValueError(suffix)

    numbers = [int(i, 16) for i in (d1, d2, d3, d4)]

    for i in reversed(range(4)):
        numbers[i] += 1
        if numbers[i] <= 255:
            break
        if i:
            numbers[i] = 0

    parts = ['%02x' % i for i in numbers]
    parts[-1] += suffix
    return os.path.join(*parts)


class Journals:
    def __init__(self, root):
        self.root = root
        self.last = last_file(root)
        if self.last:
            self.page = json.load(open(self.last))
        else:
            self._set_last(os.path.join(self.root, '00/00/00/00.json'))

    def add_hash(self, arthash):
        if len(self.page) >= 256:
            parts = os.path.relpath(self.last, self.root)
            next_parts = next_file(parts)
            self._set_last(os.path.join(self.root, next_parts))

        self.page.append([arthash, timestamp()])
        with open(self.last, 'w') as fp:
            json.dump(self.page, fp, indent=2)

    def _set_last(self, last):
        self.last = last
        self.page = []
        makedirs(os.path.dirname(last), exist_ok=True)


def timestamp():
    return datetime.datetime.utcnow().isoformat()


"""

We want to potentially store a trillion hashes but we don't want too many files
in any directory.

one trillion = 10**12 = (10**2) ** 6 = (10**3) ** 4

or (2 ** 10) ** 4 = 2 ** 40 = (2 ** 8) ** 5

So the hashes go into:

arthash.org/hashes/00/00/00/00.json
arthash.org/hashes/00/00/00/01.json
...
arthash.org/hashes/00/00/00/ff.json
arthash.org/hashes/00/00/01/00.json
arthash.org/hashes/00/00/01/01.json

Each file has 256 hashes, so the total number is:

    (256 * 256 * 256)  *    256    *      256
       directories    files/directory   hashes/file

or 1099511627776.

Now, if we actually put 256 ** 4 or 4 gig files on a filesystem there would be
trouble, but long before we got to that point, we'd have some virtual filesystem
in place which would do the trick.

If we ever get over a trillion hashes, we can easily extend the length of the
top-level directory names indefinitely - there would be a little special purpose
code for backward compatibility but `hex(dirname)` would still work perfectly
well.

"""
