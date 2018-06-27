import datetime, json, os
from . import sequence, journal_files


class Journals:
    def __init__(self, root):
        self.root = root
        self.last = sequence.last_file(root)
        if self.last:
            self.page = journal_files.read(self.last)
        else:
            self._set_last(os.path.join(self.root, '00/00/00/00.json'))

    def add_hash(self, arthash):
        if len(self.page) >= 256:
            parts = os.path.relpath(self.last, self.root)
            next_parts = sequence.next_file(parts)
            self._set_last(os.path.join(self.root, next_parts))

        self.page.append([arthash, timestamp()])
        journal_files.write(self.last, self.page)

    def _set_last(self, last):
        self.last = last
        self.page = []


def timestamp():
    return datetime.datetime.utcnow().isoformat()
