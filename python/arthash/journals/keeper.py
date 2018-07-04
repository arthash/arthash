import datetime, json, os
from . import index_files
from . import organization as org
from .. util import files


class Keeper:
    """
    Organizes all the JSON journal files and updates the HTML index files.
    """
    def __init__(self, root, organization=None):
        self.org = organization or org.Organization()
        self.root = root

        os.makedirs(root, exist_ok=True)
        self.last = files.last_file(root)

        if self.last:
            self.page = json.load(open(self.last))
        else:
            segment = self.org.digit_format % 0
            parts = '/'.join([segment] * self.org.levels)
            first = os.path.join(self.root, parts + '.json')
            self._set_last(first)

    def add_hash(self, arthash):
        if len(self.page) >= self.org.page_size:
            parts = os.path.relpath(self.last, self.root)
            next_parts = self.org.next_file(parts)
            self._set_last(os.path.join(self.root, next_parts))

        self.page.append([arthash, timestamp()])

        exists = os.path.exists(self.last)
        if not exists:
            os.makedirs(os.path.dirname(self.last), exist_ok=True)

        with open(self.last, 'w') as fp:
            json.dump(self.page, fp, indent=2)

        if not exists:
            index_files.write_indexes(self.last, self.org.levels)

    def _set_last(self, last):
        self.last = last
        self.page = []


def timestamp():
    return datetime.datetime.utcnow().isoformat()
