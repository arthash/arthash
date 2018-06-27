import datetime, json, os
from os import listdir, makedirs
from os.path import isdir
from . import index_file
from .. import files

open = __builtins__['open']


def last_file(f):
    while isdir(f):
        dfiles = [f for f in listdir(f) if files.is_journal_file(f)]
        if not dfiles:
            return
        f = os.path.join(f, sorted(dfiles)[-1])
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
        exists = os.path.exists(self.last)
        with open(self.last, 'w') as fp:
            json.dump(self.page, fp, indent=2)

        if not exists:
            index_file.add_index_file(self.last)

    def _set_last(self, last):
        self.last = last
        self.page = []
        makedirs(os.path.dirname(last), exist_ok=True)


def timestamp():
    return datetime.datetime.utcnow().isoformat()
