import datetime, json, math, os
from . import journal_files
from .. util import files


class Journals:
    def __init__(self, root, page_size=256, levels=4):
        os.makedirs(root, exist_ok=True)
        self.root = root
        self.page_size = page_size
        self.levels = levels
        self.digit_size = math.ceil(math.log2(page_size) / 4)
        self.digit_format = '%0' + str(self.digit_size) + 'x'
        self.last = files.last_file(root)
        if self.last:
            self.page = journal_files.read(self.last)
        else:
            segment = self.digit_format % 0
            parts = '/'.join([segment] * self.levels)
            self._set_last(os.path.join(self.root, parts + '.json'))

    def add_hash(self, arthash):
        if len(self.page) >= self.page_size:
            parts = os.path.relpath(self.last, self.root)
            next_parts = self.next_file(parts)
            self._set_last(os.path.join(self.root, next_parts))

        self.page.append([arthash, timestamp()])
        journal_files.write(self.last, self.page)

    def _set_last(self, last):
        self.last = last
        self.page = []

    def next_file(self, filename):
        segments = []
        for f in range(self.levels):
            filename, d = os.path.split(filename)
            segments.insert(0, d)

        root, suffix = os.path.splitext(segments[-1])
        if suffix != '.json':
            raise ValueError(suffix)
        segments[-1] = root

        numbers = [int(i, 16) for i in segments]

        for i in reversed(range(4)):
            numbers[i] += 1
            if numbers[i] <= 255:
                break
            if i:
                numbers[i] = 0

        parts = [self.digit_format % i for i in numbers]
        parts[-1] += suffix
        filename and parts.insert(0, filename)
        return os.path.join(*parts)


def timestamp():
    return datetime.datetime.utcnow().isoformat()
