import datetime, os
from . import journal_files
from . import organization as org
from .. util import files


class Keeper:
    """
    Organizes all the JSON journal files and updates the HTML index files.
    """
    def __init__(self, root, organization=None):
        self.org = organization or org.Organization()
        os.makedirs(root, exist_ok=True)
        self.root = root
        self.last = files.last_file(root)
        if self.last:
            self.page = journal_files.read(self.last)
        else:
            segment = self.org.digit_format % 0
            parts = '/'.join([segment] * self.org.levels)
            self._set_last(os.path.join(self.root, parts + '.json'))

    def add_hash(self, arthash):
        if len(self.page) >= self.org.page_size:
            parts = os.path.relpath(self.last, self.root)
            next_parts = self.org.next_file(parts)
            self._set_last(os.path.join(self.root, next_parts))

        self.page.append([arthash, timestamp()])
        journal_files.write(self.last, self.page)

    def _set_last(self, last):
        self.last = last
        self.page = []


def timestamp():
    return datetime.datetime.utcnow().isoformat()
