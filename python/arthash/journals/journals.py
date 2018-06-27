import datetime, json, os
from os import makedirs
from . import sequence, write_file


class Journals:
    def __init__(self, root):
        self.root = root
        self.last = sequence.last_file(root)
        if self.last:
            self.page = json.load(write_file.open(self.last))
        else:
            self._set_last(os.path.join(self.root, '00/00/00/00.json'))

    def add_hash(self, arthash):
        if len(self.page) >= 256:
            parts = os.path.relpath(self.last, self.root)
            next_parts = sequence.next_file(parts)
            self._set_last(os.path.join(self.root, next_parts))

        self.page.append([arthash, timestamp()])
        write_file.write_file(self.last, self.page)

    def _set_last(self, last):
        self.last = last
        self.page = []
        makedirs(os.path.dirname(last), exist_ok=True)


def timestamp():
    return datetime.datetime.utcnow().isoformat()
